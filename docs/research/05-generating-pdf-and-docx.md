Part of CV Factory by Johel Gomez Rojas — Apache License 2.0.

# 5. How to generate a PDF and a DOCX that machines read perfectly

Technical research from October 2026: about 40 sources (documentation from Textkernel, RChilli, Greenhouse, the PDF Association, poppler, pdfminer, Typst, Chromium and Microsoft) **plus our own experiments**. We generated PDFs with pdfLaTeX, XeLaTeX, Chromium, python-docx + LibreOffice and ReportLab, and extracted their text with five different readers: pdftotext, pdfminer, pdfplumber, pypdfium2 and pdf.js (the one used by the open-source OpenResume parser). The scripts are in [experiments/](experiments/).

Workday, Taleo, iCIMS and Daxtra do not publish how they read files. What is said about them here is inferred from how all readers work.

---

## 5.1 The text layer

**A PDF stores drawings of letters, not letters.** The extracted text depends on the font carrying its map from glyphs to characters (Unicode). If that map is missing or wrong, the PDF looks fine but extracts as garbage.
Source: [PDF Tools AG](https://pdf-tools.com/pdf-knowledge/extraction-text-pdf) — High.

**Failures confirmed in the experiments:**

| Problem | What happened | How to avoid it |
|---|---|---|
| "Type 3" (bitmap) fonts in LaTeX | "Efficient office" came out as `E\x1ecient o\x1ece`: useless | In LaTeX, use T1 with a full Latin font (lmodern); check with `pdffonts` |
| Ligatures (fi, fl, ff, ffi) | Chrome and XeLaTeX add them by default; pdfminer returned `Eﬃcient` with a special character, so "Efficient" no longer matches as a keyword | Turn ligatures off (`font-variant-ligatures: none` in CSS) |
| Accents in old LaTeX | "José" came out as `Jos´e` in three readers | T1 encoding or modern fonts |
| Letter-spaced text | A spaced-out heading came out as `S K I L L S` | Always use normal spacing (Greenhouse also lists this as an error) |
| Hyphenation | "sin-/gle" was split in two | Turn hyphenation off |
| Text converted to outlines | No text at all: the ATS would need OCR | Never convert text to outlines |

Sources: experiments · [TeX FAQ](https://www.sys.kth.se/docs/texlive/texmf-dist/doc/generic/FAQ-en/html/FAQ-srchpdf.html) · [pdfminer docs](https://pdfminersix.readthedocs.io/en/latest/topic/converting_pdf_to_text.html) · [Greenhouse](https://support.greenhouse.io/hc/en-us/articles/200989175-Unsuccessful-resume-parse) — High.

**Jake's Resume** (the most popular LaTeX template) adds a step to be "ATS readable", but it right-aligns dates with a table, which is exactly what breaks (see 5.2).
Source: [Jake's GitHub](https://github.com/jakegut/resume/blob/master/resume.tex).

## 5.2 Reading order (the most important finding)

**Most readers ignore the PDF's accessibility "tags".** They read in the order the content was drawn, or guess from position. The same PDF with and without tags gave exactly the same text in three readers.
Sources: [man pdftotext](https://manpages.debian.org/testing/poppler-utils/pdftotext.1.en.html) · [PDF Association](https://pdfa.org/resource/tagged-pdf-q-a/) · experiment — High.

**Right-aligned dates come apart from the job title.** We tested four ways to write a job line:

| Layout | Survives in every reader? |
|---|---|
| `Title, Company \| January 2020 – Present` (same line, with a bar) | **Yes** |
| Date on the next line | **Yes** |
| Date on the right with flexible spacing | No: pdftotext sent it **to the end of the page** |
| Date on the right with a fixed gap | No: split apart in pdftotext and pdfminer |

The same happened with Jake's Resume table and with a right tab stop in Word converted to PDF (pdfminer put the date after the first bullet).
Source: experiment reproduced with three different generators — High.
→ **Rule:** dates on the same line as the title, after a bar, or on the next line. Never right-aligned.

**Columns are still the best-documented failure.** Textkernel says reading top to bottom and left to right "mixes content from different columns"; RChilli reads the left column first and separates titles from companies; OpenResume only reads single-column CVs.
Sources: [Textkernel](https://textkernel.com/learn-support/blog/improving-extraction-from-column-resumes) · [RChilli](https://www.rchilli.com/tips-for-creating-electronics-resumes) · [OpenResume](https://www.open-resume.com/resume-parser) — High.

**The generator has to write in logical order.** In one test, drawing the date before the title made pdf.js read the date first.

**Headers and footers:** RChilli does not read them; python-docx (and many DOCX readers) ignores them completely.
Source: [RChilli](https://help.rchilli.com/hc/en-us/articles/900001627906-How-do-parser-extract-data) — High.

**Tables:** a two-column table in a DOCX was read by rows in three readers and by columns in two others. There is no safe way.
Source: experiment · [Jobscan](https://www.jobscan.co/blog/resume-tables-columns-ats/) — High.

## 5.3 Characters

| Character | Result in the experiments | Verdict |
|---|---|---|
| Icon fonts (Font Awesome, etc.) | Garbage stuck to the email and phone | **Forbidden** |
| Word's and python-docx's default bullet | It is a private-use character (U+F0B7) and came out as `` in every reader | **Replace** with a normal `•` |
| ★ ✓ ▪ symbols with non-embedded fonts | Came out as `H` and `3` | **Forbidden** |
| Emojis | Drawn with a Type 3 font; noise for contact detection | **Forbidden** |
| Zero-width spaces and soft hyphens | Split words: "JavaS cript", "Kubern etes" | **Forbidden** |
| Curly quotes, en dash (–), bullet • with a properly embedded font | Came out fine everywhere | Allowed |

Sources: experiments · [W3C](https://www.w3.org/WAI/GL/wiki/Icon_Font_with_an_On-Screen_Text_Alternative) · [Unicode](https://unicode.org/mail-arch/unicode-ml/Archives-Old/UML022/0292.html) — High.

**Also:** RChilli recommends one line per contact detail instead of separating them with symbols, and OpenResume expects a simply formatted phone number. Keep contact details in plain text, with no decoration.

## 5.4 What to generate it with

| Tool | Result | Verdict |
|---|---|---|
| HTML + CSS → Chromium (Puppeteer / Playwright) | Fonts embedded with their Unicode map; tags optional. In Playwright you have to ask for them (`tagged: true`) | **Recommended**, with ligatures off |
| Typst 0.14+ | Tagged PDF by default and a PDF/UA-1 accessibility option. Not tested locally | Good alternative (turn off ligatures and hyphenation) |
| python-docx (DOCX) | Works if you use only paragraphs, with no tables, text boxes or headers, and with your own bullet | **Recommended** for the DOCX |
| LibreOffice (DOCX → PDF) | Fine, and copies title and author into the PDF | Useful for validating the DOCX |
| ReportLab with base fonts | Does not embed fonts: symbols come out as garbage | Only with a registered TTF font |
| pdfLaTeX / XeLaTeX | Work with tweaks, but are easy to break | Not recommended |
| Export from Google Docs | Can add odd annotations in headers | Not recommended |
| Export from Word | Fine if "Document structure tags for accessibility" is checked | Acceptable |

Sources: [Chromium](https://blog.chromium.org/2020/07/using-chrome-to-generate-more.html) · [Puppeteer](https://pptr.dev/next/api/puppeteer.pdfoptions) · [Typst 0.14](https://typst.app/blog/2025/typst-0.14) · [Overleaf](https://docs.overleaf.com/writing-and-editing/creating-accessible-pdfs) · [Microsoft](https://support.microsoft.com/en-us/office/create-accessible-pdfs-064625e0-56ea-4e16-ad71-3aa33bb4b7ed) · [Boise State](https://www.boisestate.edu/accessibility/create-accessible-documents/export-to-pdf/) · experiments.

## 5.5 Metadata, size and AI readers

- **Size:** Greenhouse fails to parse files over 2.5 MB. The text-only PDFs in our tests weighed 32–36 KB. Target: under 1 MB. [Greenhouse](https://support.greenhouse.io/hc/en-us/articles/360052218132-Supported-file-types-for-resumes-and-cover-letters)
- **Metadata:** title "First Last – Resume", author set to the person's name, no leftovers from templates. File name `First-Last-Resume.pdf`.
- **AI models see both the text and an image of each page.** Claude and OpenAI extract both, so a PDF with bad text can be rescued visually, but systems that only use the text have no fallback. [Claude](https://platform.claude.com/docs/en/build-with-claude/pdf-support) · [OpenAI](https://developers.openai.com/api/docs/guides/file-inputs)
- **Accessibility tags** changed nothing in the readers we tested, but they are free in Chromium, Typst and Word, so turn them on anyway.

## 5.6 How to test each CV before sending it

**Manual test (anyone can do it):** open the PDF, select all, copy and paste into a plain text editor. It must come out in order, with whole words, each date next to its job and no strange symbols. It is the same test RChilli recommends.

**Free online "ATS scores" do not measure a real ATS:** they estimate how many words match. One open-source AI scorer, run 100 times on the same CV, gave scores from 66 to 99.
Sources: [atsverification](https://atsverification.com/blog/are-ats-checkers-accurate/) · [Workera](https://www.workera.ai/blog/the-hackerrank-open-source-ats-didnt-have-a-bug-it-had-a-measurement-error) — Medium.

**Automated tests the generator should run** (the engine runs these as tests 1–9):

1. **Fonts:** all embedded, with a Unicode map, none Type 3 (`pdffonts`).
2. **Extraction with several readers** (pdftotext, pdfminer, pdf.js, pypdfium2): 99.5 % or more of the profile's words must appear, with no forbidden characters or ligatures.
3. **Spacing and hyphens:** fail if spaced-out letters or words split at the end of a line appear.
4. **Order:** each job with its company and dates on the same line or the next; sections in the right order; name, email and phone in the first 5 lines.
5. **OpenResume parser:** it must extract name, email, phone, each job and education. (Found while building the engine: OpenResume does not recognize abbreviated months such as "Jan", drops names with accents and only reads US phone numbers. That is why the engine writes months in full. For non-English CVs this test checks only name and contact. In an English CV, an education entry without an English school or degree word that OpenResume recognizes (e.g. "SENA") is only noted, and tests 4 and 6 verify it (an entry with a keyword must be extracted); Education is never dropped. See [cv-rules.md](cv-rules.md).)
6. **AI extraction:** give the PDF and the plain text to a model, extract the data in a fixed format and compare it with the profile.
7. **Metadata and size:** title and author set, under 1 MB, at most 2 pages.
8. **DOCX:** no tables, text boxes or text in headers or footers; bullets with no private-use characters; convert it to PDF and run tests 1–4.
9. **No accents in English CVs:** no accented letters or ñ in the PDF, the DOCX, the metadata or the file name.

## 5.7 The engine

**One source, two outputs:** the CV content in a data file (`cv.json`) → HTML + CSS → PDF with Chromium, and the same file → DOCX with python-docx. Both are produced by `engine/scripts/cv.py generate`, and `engine/scripts/cv.py test` reruns the tests.

**Required CSS:**
```css
font-variant-ligatures: none;
font-feature-settings: "liga" 0, "clig" 0, "dlig" 0;
hyphens: manual;
letter-spacing: 0;
word-spacing: normal;
```

**Layout:** one column; the name as the main heading and sections as subheadings with standard names; contact details in the body, as plain text; dates inline with the title; a real embedded font (Carlito, Liberation Sans or Noto Sans, or a licensed Arial/Calibri) at 10–12 pt; no images, bars or backgrounds.

**Characters:** allow ASCII, accented letters, en dash (–), bullet (•) and curly quotes. Normalize non-breaking spaces and special hyphens. Block (and fail the build on): private-use characters, emojis, decorative symbols, invisible characters, soft hyphens and control characters.
