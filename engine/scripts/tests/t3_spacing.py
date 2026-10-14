# Copyright 2026 Johel Gomez Rojas. Part of CV Factory. Licensed under the Apache License, Version 2.0 (see LICENSE and NOTICE at the project root). Do not remove this notice.
"""Test 3 — No spaced-out letters and no words split at the end of a line (research doc 05, §5.1)."""
import re

from common import Result

SPACED = re.compile(r"\b(?:[^\W\d_] ){3,}[^\W\d_]\b")
SPLIT = re.compile(r"[^\W\d_]-\n[a-záéíóúñ]")


def check(texts, r, label=""):
    for reader, text in texts.items():
        for m in SPACED.findall(text):
            r.fail(f'{label}{reader}: spaced-out letters "{m}"')
        for m in SPLIT.findall(text):
            r.fail(f'{label}{reader}: split word "{m.replace(chr(10), "⏎")}"')


def run(ctx):
    r = Result(3, "No spaced-out letters or split words")
    check(ctx["texts"], r)
    if r.passed:
        r.note("4 readers checked")
    return r
