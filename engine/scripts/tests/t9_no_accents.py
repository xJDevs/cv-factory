# Copyright 2026 Johel Gomez Rojas. Part of CV Factory. Licensed under the Apache License, Version 2.0 (see LICENSE and NOTICE at the project root). Do not remove this notice.
"""Test 9 — English CV without accents or ñ: not in the PDF (4 readers), not in the DOCX, not in
the metadata. That way it matches what a US recruiter types ("San Jose") and it cannot turn
into garbled symbols ("JosÃ©") on a misconfigured system.
For Spanish CVs the test does not apply: accents belong there."""
import re
import unicodedata

import pikepdf
from docx import Document

from common import Result

ALLOWED = set("–—•‘’“”")


def odd(text):
    """Any character outside printable ASCII, whitespace and the allowed punctuation."""
    t = unicodedata.normalize("NFC", text)
    return sorted({c for c in t if not (0x20 <= ord(c) <= 0x7E or c in ALLOWED or c in "\n\r\t\x0c")})


def describe(cs):
    return ", ".join(f'"{c}" U+{ord(c):04X}' for c in cs[:8])


def run(ctx):
    r = Result(9, "English CV without accents or ñ")
    if ctx["view"]["language"] != "en":
        r.note("Spanish CV: accents belong there; the test does not apply")
        return r
    for reader, text in ctx["texts"].items():
        cs = odd(text)
        if cs:
            r.fail(f"PDF ({reader}): {describe(cs)}")
    doc = Document(ctx["docx"])
    docx_text = "\n".join(p.text for p in doc.paragraphs)
    docx_text += "\n" + (doc.core_properties.title or "") + "\n" + (doc.core_properties.author or "")
    cs = odd(docx_text)
    if cs:
        r.fail(f"DOCX: {describe(cs)}")
    with pikepdf.open(ctx["pdf"]) as pdf:
        meta = " ".join(str(pdf.docinfo.get(k, "")) for k in ("/Title", "/Author", "/Subject"))
    cs = odd(meta)
    if cs:
        r.fail(f"PDF metadata: {describe(cs)}")
    if not re.fullmatch(r"[A-Za-z0-9-]+", ctx["base"]):
        r.fail(f"file name with odd characters: {ctx['base']}")
    if r.passed:
        r.note("no accented letters or ñ in the PDF, the DOCX, the metadata or the file name")
    return r
