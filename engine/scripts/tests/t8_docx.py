# Copyright 2026 Johel Gomez Rojas. Part of CV Factory. Licensed under the Apache License, Version 2.0 (see LICENSE and NOTICE at the project root). Do not remove this notice.
"""Test 8 — DOCX: no tables, text boxes or text in headers/footers, bullets without private
characters, the same text through two paths, and converted to PDF it passes tests 1–4."""
import re
import subprocess
import tempfile
import zipfile
from pathlib import Path

from docx import Document

import t1_fonts
import t2_extraction
import t3_spacing
import t4_order
from common import TEXT, Result, extract_all, recall
from platform_tools import require
from render_docx import FONT

XML_TEXT = re.compile(r"<w:t(?:\s[^>]*)?>([^<]*)</w:t>")


def raw_text(z):
    """Like docx2txt: all the text of the document, headers and footers."""
    parts = [n for n in z.namelist() if re.match(r"word/(document|header\d*|footer\d*)\.xml", n)]
    out = []
    for n in parts:
        for paragraph in z.read(n).decode("utf-8").split("</w:p>"):
            out.append("".join(XML_TEXT.findall(paragraph)))
    return "\n".join(out)


def run(ctx):
    r = Result(8, "Clean, convertible DOCX")
    path = ctx["docx"]
    with zipfile.ZipFile(path) as z:
        doc_xml = z.read("word/document.xml").decode("utf-8")
        if "<w:tbl" in doc_xml:
            r.fail("the DOCX has tables")
        if "txbxContent" in doc_xml:
            r.fail("the DOCX has text boxes")
        for n in z.namelist():
            if re.match(r"word/(header|footer)\d*\.xml", n) and XML_TEXT.search(z.read(n).decode("utf-8")):
                r.fail(f"{n} has text (contact details never go in a header or footer)")
        if "word/numbering.xml" in z.namelist():
            check_bullets(z.read("word/numbering.xml").decode("utf-8"), doc_xml, r)
        raw = raw_text(z)
    paragraphs = "\n".join(p.text for p in Document(path).paragraphs)
    target = "\n".join(ctx["expected"])
    pct_raw, missing_raw = recall(target, raw)
    pct_par, missing_par = recall(target, paragraphs)
    missing = sorted(set(missing_raw) | set(missing_par))
    if min(pct_raw, pct_par) < t2_extraction.MINIMUM:
        r.fail(f"DOCX text incomplete: raw {pct_raw:.1f} %, paragraphs {pct_par:.1f} % (missing: {', '.join(missing[:8])})")
    elif abs(pct_raw - pct_par) > 0.01:
        r.fail("the raw text and the paragraph text do not match: there is text hidden outside the paragraphs")
    else:
        r.note(f"complete text through both paths ({pct_par:.1f} %)")
    convert_and_check(path, ctx, r)
    return r


def check_bullets(num_xml, doc_xml, r):
    """The bullets the document uses cannot have private-use characters (U+F0B7)."""
    used = set(re.findall(r'<w:numId w:val="(\d+)"', doc_xml))
    abstracts = {m.group(1): m.group(2) for m in re.finditer(
        r'<w:num w:numId="(\d+)"[^>]*>.*?<w:abstractNumId w:val="(\d+)"', num_xml, re.S)}
    for nid in used:
        aid = abstracts.get(nid)
        block = re.search(rf'<w:abstractNum [^>]*w:abstractNumId="{aid}".*?</w:abstractNum>', num_xml, re.S)
        if not block:
            r.fail(f"list {nid} has no definition")
            continue
        for txt in re.findall(r'<w:lvlText w:val="([^"]*)"', block.group(0)):
            if any(0xE000 <= ord(c) <= 0xF8FF for c in txt):
                r.fail(f"the bullet of list {nid} uses a private-use character ({txt!r})")
    if used:
        r.note(f"bullets checked in {len(used)} list(s)")


def convert_and_check(path, ctx, r):
    # ignore_cleanup_errors: on Windows LibreOffice may still hold its profile for a moment.
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp:
        # Its own LibreOffice profile, so an open LibreOffice window cannot take over the conversion.
        profile = (Path(tmp) / "lo-profile").as_uri()
        subprocess.run([require("soffice"), f"-env:UserInstallation={profile}", "--headless",
                        "--convert-to", "pdf", "--outdir", tmp, str(path)],
                       timeout=180, check=True, **TEXT)
        pdf = Path(tmp) / (Path(path).stem + ".pdf")
        if not pdf.exists():
            r.fail("LibreOffice could not convert the DOCX to PDF")
            return
        texts = extract_all(pdf)
        # The DOCX names Calibri. Where Calibri is installed (Windows), LibreOffice embeds it;
        # elsewhere it uses Carlito, its metric-compatible twin. Either one is the CV font.
        t1_fonts.check(pdf, r, "DOCX→PDF ", families=(t1_fonts.FAMILY, FONT))
        t2_extraction.check(texts, ctx["expected"], r, "DOCX→PDF ")
        t3_spacing.check(texts, r, "DOCX→PDF ")
        t4_order.check(texts, ctx["view"], r, "DOCX→PDF ")
        # The bullet used must come out as • and not as U+F0B7
        if any("" in t for t in texts.values()):
            r.fail("DOCX→PDF: the bullet came out as U+F0B7 (Word's Symbol bullet)")
