# Copyright 2026 Johel Gomez Rojas. Part of CV Factory. Licensed under the Apache License, Version 2.0 (see LICENSE and NOTICE at the project root). Do not remove this notice.
"""The CV engine: data → PDF + DOCX → 9 tests (the 8 of research doc 05, §5.6 + no accents in
English). No CV is delivered if anything fails.

Usage:
  python3 cv.py generate <cv.json> --snapshot <snapshot.json> --out <folder>
  python3 cv.py test     <cv.json> --snapshot <snapshot.json> --out <folder>

"generate" creates the PDF and the DOCX (and deletes old test 6 results, because they are no
longer valid for the new file) and then runs the tests. "test" only runs the tests.
Exits with code 0 only if the pre-checks and the 9 tests pass.

If the project root (the parent of engine/) has a project.json with "cv_languages": [...],
a cv.json whose language is not in that list fails the pre-check.
"""
import argparse
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(HERE / "tests")]

import data  # noqa: E402
import platform_tools  # noqa: E402
import render_docx  # noqa: E402
import render_pdf  # noqa: E402
import traceability  # noqa: E402
from common import Result, extract_all  # noqa: E402
import t1_fonts, t2_extraction, t3_spacing, t4_order  # noqa: E402,E401
import t5_openresume, t6_ai, t7_meta, t8_docx, t9_no_accents  # noqa: E402,E401

TESTS = [t1_fonts, t2_extraction, t3_spacing, t4_order, t5_openresume, t6_ai, t7_meta, t8_docx,
         t9_no_accents]
PROJECT_FILE = data.ROOT.parent / "project.json"
AI_RESULTS = ("ai-from-pdf.json", "ai-from-text.json")


def check_allowed_language(cv, errors):
    """Optional project.json at the project root: "cv_languages" limits the CV languages."""
    if not PROJECT_FILE.exists():
        return
    try:
        allowed = json.loads(PROJECT_FILE.read_text(encoding="utf-8-sig")).get("cv_languages")
    except (ValueError, AttributeError) as e:
        errors.append(f"project.json could not be read ({e}); fix it or remove it")
        return
    if allowed is None:
        return
    language = cv.get("language", "en")
    if language not in allowed:
        errors.append(f"language '{language}' is not allowed in this project "
                      f"(project.json \"cv_languages\": {', '.join(allowed) or 'none'})")


def main():
    ap = argparse.ArgumentParser(description="Generate a CV (PDF + DOCX) and run the 9 tests.")
    ap.add_argument("action", choices=["generate", "test"])
    ap.add_argument("cv", help="path of cv.json")
    ap.add_argument("--snapshot", required=True, help="snapshot.json of the source data, read live")
    ap.add_argument("--out", required=True, help="output folder")
    a = ap.parse_args()
    folder = Path(a.out).resolve()
    folder.mkdir(parents=True, exist_ok=True)

    cv, view, errors = data.load(a.cv)
    check_allowed_language(cv, errors)
    pre = traceability.run(cv, a.snapshot)
    data_ok = Result(0, "Complete data and allowed characters")
    for e in errors:
        data_ok.fail(e)
    if not (pre.passed and data_ok.passed):
        return report(folder, [data_ok, pre], generated=False)

    base = data.file_name(view)
    if a.action == "generate":
        for old in AI_RESULTS:
            (folder / old).unlink(missing_ok=True)
        try:
            render_pdf.generate(view, folder, base)
            render_docx.generate(view, folder, base)
        except RuntimeError as e:
            data_ok.fail(f"could not generate: {e}")
            return report(folder, [data_ok, pre], generated=False)
    pdf, docx = folder / f"{base}.pdf", folder / f"{base}.docx"
    if not (pdf.exists() and docx.exists()):
        data_ok.fail('the PDF and the DOCX do not exist: run "generate" first')
        return report(folder, [data_ok, pre], generated=False)

    texts = extract_all(pdf)
    (folder / "plain-text.txt").write_text(texts["pdftotext"], encoding="utf-8", newline="\n")
    ctx = {"cv": cv, "view": view, "pdf": pdf, "docx": docx, "base": base, "folder": folder,
           "texts": texts, "expected": data.expected_text(view)}
    results = [data_ok, pre]
    for test in TESTS:
        try:
            results.append(test.run(ctx))
        except (subprocess.SubprocessError, OSError, ValueError, KeyError) as e:
            r = Result(int(test.__name__[1]), test.__name__)
            r.fail(f"the test crashed: {e}")
            results.append(r)
    return report(folder, results, generated=True)


def report(folder, results, generated):
    all_ok = generated and all(r.passed for r in results)
    lines = [f"# Test report — {datetime.now():%Y-%m-%d %H:%M}", "",
             f"**Result: {'APPROVED — ready to deliver' if all_ok else 'NOT APPROVED — do not deliver'}**", ""]
    for r in results:
        mark = "✅" if r.passed else "❌"
        lines.append(f"## {mark} {'Pre-check' if r.number == 0 else f'Test {r.number}'}: {r.name}")
        lines += [f"- ❌ {f}" for f in r.failures] + [f"- {n}" for n in r.notes] + [""]
    (folder / "test-report.md").write_text("\n".join(lines), encoding="utf-8", newline="\n")
    print("\n".join(lines))
    return 0 if all_ok else 1


if __name__ == "__main__":
    platform_tools.utf8_console()
    sys.exit(main())
