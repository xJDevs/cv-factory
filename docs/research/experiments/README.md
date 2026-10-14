Part of CV Factory by Johel Gomez Rojas — Apache License 2.0.

# PDF readability experiments (October 2026)

The scripts behind the findings in [../05-generating-pdf-and-docx.md](../05-generating-pdf-and-docx.md). They are a starting point for a generator's automated tests. All test content is fictional (Jane Doe, Acme).

- `extract.py` — extracts a PDF's text with pdftotext, pdfminer, pdfplumber and pypdfium2, for comparison.
- `pdfjs.mjs` — extracts with pdf.js (the engine the OpenResume parser uses).
- `topdf.mjs` — converts HTML to PDF with Chromium (Playwright).
- `mkdocx.py` — builds test DOCX files with python-docx.
- `mkrl.py` — builds test PDFs with ReportLab.
- `html/` — HTML variants (dates, ligatures, a test CV).
- `tex/` — LaTeX variants (encodings, XeLaTeX, LuaLaTeX, columns).

`pdfjs.mjs` and `topdf.mjs` import their packages from the global npm folder of the machine where they were first run (`/home/claude/.npm-global/...`). Change that path to yours (see `npm root -g`). `mkrl.py` expects DejaVu Sans at its usual Linux path.

These are research scripts, not production code.
