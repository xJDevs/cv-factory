# Copyright 2026 Johel Gomez Rojas. Part of CV Factory. Licensed under the Apache License, Version 2.0 (see LICENSE and NOTICE at the project root). Do not remove this notice.
"""View → HTML (template) → PDF with Chromium, plus metadata with pikepdf."""
from pathlib import Path

import re

import jinja2
import markupsafe
import pikepdf
from playwright.sync_api import sync_playwright

from data import ROOT

PAPERS = {"letter": "Letter", "a4": "A4"}


def no_hyphen_breaks(text):
    """A hyphenated word ("return-to-work", "data-driven") never breaks at the end of a line:
    pdfium reads the break as U+FFFE and pdf.js as a split word (tests 3 and 9)."""
    safe = str(markupsafe.escape(text))
    return markupsafe.Markup(re.sub(r"\S+-\S+", lambda m: f'<span class="nobr">{m.group(0)}</span>', safe))


def html(view):
    templates = ROOT / "template"
    css = (templates / "cv.css").read_text(encoding="utf-8")
    css = css.replace("{{FONTS}}", (ROOT / "fonts").as_uri())
    css = css.replace("{{PAPER}}", PAPERS.get(view["paper"], "Letter"))
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(templates), autoescape=True)
    env.filters["nobr"] = no_hyphen_breaks
    return env.get_template("cv.html.j2").render(v=view, css=css)


def generate(view, folder, base):
    folder = Path(folder)
    folder.mkdir(parents=True, exist_ok=True)
    html_path = folder / f"{base}.html"
    pdf_path = folder / f"{base}.pdf"
    html_path.write_text(html(view), encoding="utf-8", newline="\n")
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(html_path.as_uri(), wait_until="networkidle")
        page.evaluate("document.fonts.ready")
        # If the CV font did not load, Chromium silently uses another one: stop here.
        loaded = page.evaluate("[...document.fonts].filter(f => f.status === 'loaded').map(f => f.family)")
        family = page.evaluate("getComputedStyle(document.body).fontFamily")
        if not any("CV" in f for f in loaded) or not family.startswith('"CV"') and not family.startswith("CV"):
            browser.close()
            raise RuntimeError(f"the Carlito font did not load (body font family: {family}; loaded: {loaded})")
        page.pdf(path=str(pdf_path), prefer_css_page_size=True, tagged=True,
                 outline=False, print_background=False)
        browser.close()
    with pikepdf.open(pdf_path, allow_overwriting_input=True) as pdf:
        with pdf.open_metadata() as meta:
            meta["dc:title"] = view["pdf_title"]
            meta["dc:creator"] = [view["name"]]
        pdf.docinfo["/Title"] = view["pdf_title"]
        pdf.docinfo["/Author"] = view["name"]
        pdf.docinfo["/Subject"] = view["headline"]
        pdf.Root.Lang = pikepdf.String(view["language"])
        pdf.save(pdf_path)
    return pdf_path
