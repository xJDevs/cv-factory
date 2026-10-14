# Copyright 2026 Johel Gomez Rojas. Part of CV Factory. Licensed under the Apache License, Version 2.0 (see LICENSE and NOTICE at the project root). Do not remove this notice.
"""Test 4 — Order: each job with its company and dates together, sections in order,
name/email/phone at the top (research doc 05, §5.2)."""
import unicodedata

from common import Result, lines


def norm(t):
    return " ".join(unicodedata.normalize("NFC", t).lower().split())


def check(texts, view, r, label=""):
    contact = [view["name"]] + [c for c in view["contact"] if "@" in c or any(ch.isdigit() for ch in c)]
    for reader, text in texts.items():
        ls = [norm(l) for l in lines(text)]
        top = " ".join(ls[:5])
        for item in contact:
            if norm(item) not in top:
                r.fail(f'{label}{reader}: "{item}" is not in the first 5 lines')
        pos = -1
        for s in view["sections"]:
            idx = next((i for i, l in enumerate(ls) if i > pos and l == norm(s["title"])), None)
            if idx is None:
                r.fail(f'{label}{reader}: the section "{s["title"]}" is not alone on its line or is out of order')
                continue
            pos = idx
            check_entries(ls, s, idx, reader, r, label)


def check_entries(ls, section, start, reader, r, label):
    i0 = start
    for e in section.get("entries", []):
        title = norm(e["bold"])
        idx = next((i for i in range(i0, len(ls)) if title in ls[i]), None)
        if idx is None:
            r.fail(f'{label}{reader}: "{e["bold"]}" was not found')
            continue
        block = ls[idx] + " " + (ls[idx + 1] if idx + 1 < len(ls) else "")
        company = e["rest"].lstrip(", ").split(", ")[0] if e["rest"] else ""
        for part, what in ((company, "company/detail"), (e["dates"], "dates")):
            if part and norm(part) not in block:
                r.fail(f'{label}{reader}: "{e["bold"]}" got separated from its {what} "{part}"')
        i0 = idx + 1


def run(ctx):
    r = Result(4, "Reading order and title–company–dates association")
    check(ctx["texts"], ctx["view"], r)
    if r.passed:
        n = sum(len(s.get("entries", [])) for s in ctx["view"]["sections"])
        r.note(f"{n} entries and {len(ctx['view']['sections'])} sections in order in the 4 readers")
    return r
