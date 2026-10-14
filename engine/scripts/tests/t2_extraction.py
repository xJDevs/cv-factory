# Copyright 2026 Johel Gomez Rojas. Part of CV Factory. Licensed under the Apache License, Version 2.0 (see LICENSE and NOTICE at the project root). Do not remove this notice.
"""Test 2 — Extraction with 4 readers: ≥ 99.5 % of the words and no forbidden characters."""
from common import Result, forbidden_chars, recall

MINIMUM = 99.5


def check(texts, expected, r, label=""):
    target = "\n".join(expected)
    for reader, text in texts.items():
        pct, missing = recall(target, text)
        if pct < MINIMUM:
            r.fail(f"{label}{reader}: {pct:.1f} % of the words (missing: {', '.join(missing[:10])})")
        else:
            r.note(f"{label}{reader}: {pct:.1f} %")
        for desc, examples in forbidden_chars(text):
            r.fail(f"{label}{reader}: {desc} → {examples}")


def run(ctx):
    r = Result(2, "Extraction with pdftotext, pdfminer, pdf.js and pdfium")
    check(ctx["texts"], ctx["expected"], r)
    return r
