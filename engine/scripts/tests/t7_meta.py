# Copyright 2026 Johel Gomez Rojas. Part of CV Factory. Licensed under the Apache License, Version 2.0 (see LICENSE and NOTICE at the project root). Do not remove this notice.
"""Test 7 — Metadata and size: title, author, language, < 1 MB, at most 2 pages (research doc 05, §5.5)."""
import pikepdf

from common import Result

LIMIT = 1_000_000


def run(ctx):
    r = Result(7, "Metadata, size and pages")
    pdf, view = ctx["pdf"], ctx["view"]
    size = pdf.stat().st_size
    (r.fail if size >= LIMIT else r.note)(f"size {size / 1024:.0f} KB")
    with pikepdf.open(pdf) as doc:
        pages = len(doc.pages)
        (r.fail if pages > 2 else r.note)(f"{pages} page(s)")
        info = doc.docinfo
        for key, want in (("/Title", view["pdf_title"]), ("/Author", view["name"])):
            value = str(info.get(key, ""))
            if value != want:
                r.fail(f'{key} is "{value}", it should be "{want}"')
        if str(doc.Root.get("/Lang", "")) != view["language"]:
            r.fail("the document language (/Lang) is missing")
        if "/StructTreeRoot" not in doc.Root:
            r.note("warning: the PDF is not tagged (does not block)")
        else:
            r.note("tagged PDF")
    if pdf.name != ctx["base"] + ".pdf":
        r.fail(f'file name "{pdf.name}" should be "{ctx["base"]}.pdf" (every part of the name, no accents, '
               'ending in -Resume for English CVs and -CV for Spanish ones)')
    return r
