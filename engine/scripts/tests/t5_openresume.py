# Copyright 2026 Johel Gomez Rojas. Part of CV Factory. Licensed under the Apache License, Version 2.0 (see LICENSE and NOTICE at the project root). Do not remove this notice.
"""Test 5 — OpenResume parser: it must correctly extract name, email, phone, every job
and the education (research doc 05, §5.6). OpenResume is AGPL-3.0: it is downloaded separately
at runtime and never shipped with the engine."""
import json
import os
import re
import subprocess
import tempfile
import unicodedata
from pathlib import Path

from common import TEXT, Result, pdfjs_root, tsx_command
from platform_tools import cache_dir, require
from t4_order import norm

REPO = "https://github.com/xitanggg/open-resume.git"
COMMIT = "4f8255a2c763479837f69f1dccf2a3338730cd79"
CACHE = cache_dir() / "cv-factory" / "open-resume"  # ~/.cache, $XDG_CACHE_HOME or %LOCALAPPDATA%
ADAPTER = Path(__file__).resolve().parent.parent / "openresume"


def prepare():
    if not (CACHE / "src").exists():
        CACHE.parent.mkdir(parents=True, exist_ok=True)
        git = require("git")
        subprocess.run([git, "clone", "--quiet", REPO, str(CACHE)], check=True, timeout=120)
        subprocess.run([git, "-C", str(CACHE), "checkout", "--quiet", COMMIT], check=True)
    return CACHE


def parse(pdf):
    repo = prepare()
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp:
        tsconfig = Path(tmp) / "tsconfig.json"
        # Forward slashes work in Node on every system; json.dumps keeps the file valid JSON.
        tsconfig.write_text(json.dumps({"compilerOptions": {
            "baseUrl": (repo / "src" / "app").as_posix(), "paths": {
                "lib/redux/resumeSlice": [(ADAPTER / "resume-slice-minimal.ts").as_posix()],
                "lib/*": ["lib/*"]},
            "module": "esnext", "moduleResolution": "bundler", "target": "es2022"}}), encoding="utf-8")
        output = subprocess.run(
            tsx_command() + ["--tsconfig", str(tsconfig), str(ADAPTER / "run.ts"), str(pdf)],
            timeout=180, env={**os.environ, "PDFJS_ROOT": pdfjs_root()}, **TEXT)
    if output.returncode != 0:
        raise RuntimeError(output.stderr[-800:])
    return json.loads(output.stdout)


def plain(t):
    """Same as the adapter: no accents, to compare with what OpenResume sees."""
    return norm(unicodedata.normalize("NFD", t or "").encode("ascii", "ignore").decode())


def digits(t):
    return re.sub(r"\D", "", t or "")


def run(ctx):
    r = Result(5, "OpenResume parser (name, contact, jobs, education)")
    try:
        parsed = parse(ctx["pdf"])
    except Exception as e:  # without the parser, the test does not pass
        r.fail(f"could not run OpenResume: {e}")
        return r
    res, c = parsed["result"], ctx["cv"]["contact"]
    profile = res.get("profile", {})
    if plain(profile.get("name", "")) != plain(c["name"]):
        r.fail(f'name: extracted "{profile.get("name")}"')
    if norm(profile.get("email", "")) != norm(c["email"]):
        r.fail(f'email: extracted "{profile.get("email")}"')
    phone = digits(c.get("phone"))
    if phone and (len(phone) == 10 or (len(phone) == 11 and phone[0] == "1")):
        if phone[-10:] not in digits(profile.get("phone")):
            r.fail(f'phone: extracted "{profile.get("phone")}"')
    elif phone:
        r.note("phone outside the US: OpenResume only recognizes 10-digit US numbers; "
               "the phone is checked in tests 4 and 6")
    if ctx["view"]["language"] == "en":
        check_jobs(res.get("workExperiences", []), ctx["cv"].get("experience", []), r)
        check_education(res.get("educations", []), ctx["cv"].get("education", []), r)
    else:
        # OpenResume only finds sections by their English titles (EXPERIENCE, EDUCATION), so in
        # other languages it cannot see jobs or education however well the PDF reads. Name and
        # contact are still checked here; jobs and education are covered by tests 4 and 6.
        r.note("CV not in English: OpenResume only recognizes English section titles, so this test "
               "checks name and contact; jobs and education are verified by tests 4 and 6")
    if r.passed:
        r.note(f"sections detected: {', '.join(parsed['sections'])}")
    return r


def check_jobs(extracted, expected, r):
    if len(extracted) != len(expected):
        r.fail(f"detected {len(extracted)} jobs, there are {len(expected)}")
    for i, e in enumerate(expected):
        s = extracted[i] if i < len(extracted) else {}
        joined = plain(" ".join([s.get("jobTitle", ""), s.get("company", ""), s.get("date", "")]))
        for part in (e["title"], e["company"]):
            if plain(part) not in joined:
                r.fail(f'job {i + 1}: did not extract "{part}" (extracted "{joined}")')
        year = (e.get("start") or "")[:4]
        if year and year not in s.get("date", ""):
            r.fail(f'job {i + 1}: did not extract the date (extracted "{s.get("date", "")}")')


# OpenResume's own keyword lists (src/app/lib/parse-resume-from-pdf/extract-resume-from-sections/
# extract-education.ts at the pinned commit). They are case-sensitive, like in OpenResume.
SCHOOLS = ("College", "University", "Institute", "School", "Academy", "BASIS", "Magnet")
DEGREES = ("Associate", "Bachelor", "Master", "PhD", "Ph.")
DEGREE_ABBREVIATION = re.compile(r"[ABM][A-Z.]")      # AA, B.S., MBA, ...


def openresume_keyword(text):
    """True if OpenResume can recognize the text as a school or a degree."""
    text = text or ""
    return (any(k in text for k in SCHOOLS) or any(k in text for k in DEGREES)
            or bool(DEGREE_ABBREVIATION.search(text)))


def check_education(extracted, expected, r):
    """An entry whose institution and degree have no English school or degree keyword is invisible
    to OpenResume however well the PDF reads ("Servicio Nacional de Aprendizaje (National Learning
    Service)"): it is noted, not failed, and tests 4 and 6 verify it. Any other entry must be found."""
    found = [plain(" ".join([s.get("school", ""), s.get("degree", "")])) for s in extracted]
    for i, e in enumerate(expected):
        if not (openresume_keyword(e.get("institution")) or openresume_keyword(e.get("degree"))):
            r.note(f'education {i + 1}: OpenResume does not recognize "{e["institution"]}" (no English '
                   'school/degree keyword); education is verified by tests 4 and 6')
            continue
        if not any(plain(e["institution"]) in joined or plain(e["degree"]) in joined for joined in found):
            r.fail(f'education {i + 1}: did not extract "{e["degree"]}" or "{e["institution"]}" '
                   f'(extracted "{" / ".join(found)}")')
