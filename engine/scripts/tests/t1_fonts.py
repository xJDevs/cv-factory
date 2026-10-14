# Copyright 2026 Johel Gomez Rojas. Part of CV Factory. Licensed under the Apache License, Version 2.0 (see LICENSE and NOTICE at the project root). Do not remove this notice.
"""Test 1 — Fonts: all embedded, with a Unicode map, none Type 3 (research doc 05, §5.1), and all
from the CV family (Carlito, with Calibri's metrics). If another one shows up, the template did not load."""
import subprocess

from common import TEXT, Result
from platform_tools import require

FAMILY = "Carlito"


def check(pdf, r, label="", families=(FAMILY,)):
    output = subprocess.run([require("pdffonts"), str(pdf)], check=True, **TEXT).stdout
    rows = output.splitlines()[2:]
    if not rows:
        r.fail(f"{label}no fonts: the PDF has no text layer")
    for row in rows:
        parts = row.split()
        if len(parts) < 6:
            continue
        name, emb, uni = parts[0], parts[-5], parts[-3]
        family = name.split("+", 1)[-1]
        if not family.startswith(families):
            r.fail(f"{label}{name}: wrong font (it must be {' or '.join(families)}); "
                   "the template or the conversion did not load it")
        if "Type 3" in row:
            r.fail(f"{label}{name}: Type 3 font (bitmap)")
        if emb != "yes":
            r.fail(f"{label}{name}: not embedded")
        if uni != "yes":
            r.fail(f"{label}{name}: no Unicode map")
    r.note(f"{label}{len(rows)} fonts checked")


def run(ctx):
    r = Result(1, "Fonts embedded, with Unicode, no Type 3")
    check(ctx["pdf"], r)
    return r
