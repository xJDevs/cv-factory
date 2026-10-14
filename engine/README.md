# CV engine

Every CV comes out of here. Nothing is assembled by hand. If any test fails, the CV is not delivered: fix it and run all the tests again.

The engine takes a `cv.json` (what the CV says, with the source row of every claim) and a `snapshot.json` (a complete, live reading of the person's data), checks that every claim is traceable to confirmed data, renders a PDF (Chromium) and a DOCX (python-docx), and runs 9 tests that check the files the way applicant tracking systems, parsers and AI readers will read them.

## What is here

| Path | What it is |
|---|---|
| `setup.py` | Gets a macOS, Linux or Windows machine ready (local `.venv` and `.node`, Chromium, system programs). Ends with `READY` or `NOT READY: ...`. `setup.sh` only runs it, so older instructions still work |
| `template/` | `cv.html.j2` and `cv.css` (single column, Carlito, no tables or icons) and `strings.json` (section titles and month names in English and Spanish) |
| `fonts/` | Carlito, with the same metrics as Calibri (OFL license, see `fonts/OFL.txt`). It is embedded in the PDF |
| `scripts/cv.py` | The only entry point: `generate` (PDF + DOCX + tests) and `test` (tests only) |
| `scripts/data.py` | Loads `cv.json`, applies the allowed-character list, strips accents if the CV is in English and builds the reading order |
| `scripts/traceability.py` | Pre-check: every sentence of the CV comes from a snapshot row, and achievements are verified |
| `scripts/build_snapshot.py` | Builds `snapshot.json` from a complete reading of the three source databases |
| `scripts/workbook.py` | Spreadsheet source: creates the person's Excel workbook from a spec, adds or updates rows (`upsert`) and reads it into the format `build_snapshot.py` takes |
| `scripts/platform_tools.py` | Finds the programs the engine runs (in PATH and in the usual install folders of each system), the engine's Python and the local Node packages, the same way on every system |
| `scripts/integrity.py` | Compares the engine files with `MANIFEST.sha256` (warns only) |
| `scripts/tests/` | The pre-check helpers and tests 1–9, `pdfjs_text.mjs` and `t6_instructions.md` |
| `scripts/openresume/` | A small adapter of our own that runs the OpenResume parser from Node |
| `example/` | A fictional person (Ana María Solís Vargas) to try the engine without real data: `cv-example.json` (English CV) and `cv-example-es.json` (the same CV in Spanish), both traced to `snapshot-example.json`. `example/output/` is the approved English result and `example/output/es/` the approved Spanish one, each with its two test 6 AI result files (without the `.html`, which holds absolute local paths to the fonts) |

## Requirements

Works on **macOS, Linux and Windows 10/11**. Tested on macOS; Windows and Linux are covered by the CI workflow (`.github/workflows/engine.yml` in cv-factory).

- **Python 3.10 or newer** (the system one, only to run `setup.py`). The engine itself runs in `engine/.venv` with `jinja2`, `playwright`, `pikepdf`, `python-docx`, `pdfminer.six`, `pypdfium2`, `openpyxl` (pinned versions are in `setup.py`).
- Chromium for Playwright (downloaded by `setup.py`).
- `poppler` (`pdftotext`, `pdffonts`), LibreOffice (`soffice`), Node (`node`, `npx`, `npm`) and `git`.
- Node packages `pdfjs-dist@5.7.284` and `tsx@4.21.0`, installed in `engine/.node`.

How to install the system programs:

| | macOS (Homebrew) | Linux (apt) | Windows (winget, in PowerShell) |
|---|---|---|---|
| Python | `brew install python` | `sudo apt install python3 python3-venv` | `winget install -e --id Python.Python.3.13` |
| Node | `brew install node` | `sudo apt install nodejs npm` | `winget install -e --id OpenJS.NodeJS.LTS` |
| poppler | `brew install poppler` | `sudo apt install poppler-utils` | `winget install -e --id oschwartz10612.Poppler` |
| LibreOffice | `brew install --cask libreoffice` | `sudo apt install libreoffice-writer fonts-crosextra-carlito` | `winget install -e --id TheDocumentFoundation.LibreOffice` |
| git | `xcode-select --install` | `sudo apt install git` | `winget install -e --id Git.Git` |

Windows notes:

- Open a **new** terminal (and restart the agent) after installing, so the new programs are in PATH. The engine also looks in the usual install folders: LibreOffice is never added to PATH (`C:\Program Files\LibreOffice\program\soffice.exe` is found on its own), and neither is Node right after installing (`C:\Program Files\nodejs`).
- **poppler:** the winget package is a copy of the [poppler-windows](https://github.com/oschwartz10612/poppler-windows/releases) release. If winget is not available, download the latest release zip, unzip it anywhere (for example `C:\poppler`) and set `CVF_POPPLER_BIN` to the folder that has `pdftotext.exe` (`...\poppler-<version>\Library\bin`): `setx CVF_POPPLER_BIN "C:\poppler\poppler-<version>\Library\bin"`, then open a new terminal. `CVF_POPPLER_BIN` works on every system and is checked before PATH. conda-forge (`conda install -c conda-forge poppler`) also works. **Do not use Chocolatey's `poppler` package:** its `pdftotext` joins section titles with the next paragraph, so tests 4 and 8 always fail; `setup.py` checks the installed `pdftotext` on the example PDF and says so.
- **Claude Code on Windows needs Git for Windows** (it runs its commands in Git Bash). The engine itself only needs `git` to download OpenResume once (test 5).
- With Calibri installed (it comes with Windows), LibreOffice embeds Calibri when test 8 converts the DOCX; elsewhere it uses Carlito, its metric-compatible twin. Test 8 accepts either one.

Run once (and again whenever something is missing), from the project folder (the one that contains `engine/`):

```
python3 engine/setup.py          # macOS / Linux
py engine\setup.py               # Windows (or: python engine\setup.py)
```

`bash engine/setup.sh` still works on macOS and Linux (it only runs `setup.py`).

It creates `engine/.venv` (never installs globally) and `engine/.node`, installs only what is missing, downloads Chromium with Playwright if it does not launch (except in environments with preinstalled browsers in `/opt/pw-browsers`), prints an install hint for each missing system program, runs the integrity check, prints the exact command to run the engine on this machine, and ends with `READY` (exit code 0) or `NOT READY: ...` (exit code 1).

The tests look for `pdfjs-dist` and `tsx` in `engine/.node` first (`engine/.node/lib/node_modules` on macOS and Linux, `engine\.node\node_modules` on Windows), and fall back to the global npm folder (`npm root -g`) and `npx --yes tsx`.

**OpenResume** is AGPL-licensed, so it is never included here. Test 5 downloads it the first time to `~/.cache/cv-factory/open-resume` (or `$XDG_CACHE_HOME/cv-factory/open-resume`; on Windows `%LOCALAPPDATA%\cv-factory\open-resume`) and pins it to commit `4f8255a2c763479837f69f1dccf2a3338730cd79` of `https://github.com/xitanggg/open-resume.git`.

## Usage

Always run the scripts with the engine's Python. In this README, **`<PY>`** stands for it:

| System | `<PY>` |
|---|---|
| macOS, Linux | `engine/.venv/bin/python` |
| Windows | `engine\.venv\Scripts\python.exe` |

(`setup.py` prints the right one at the end, as `Run the engine with: ...`.) Forward slashes in the other paths also work on Windows, so the commands below are written once:

```
<PY> engine/scripts/cv.py generate <cv.json> --snapshot <snapshot.json> --out <folder>
<PY> engine/scripts/cv.py test     <cv.json> --snapshot <snapshot.json> --out <folder>
```

- `generate` creates the PDF and the DOCX (plus the `.html` it was rendered from), deletes old test 6 results (they are not valid for a new file), writes `plain-text.txt`, and runs all the tests.
- **File names:** every part of the person's name joined with hyphens, then `-Resume` for English CVs or `-CV` for Spanish ones: `Ana-Maria-Solis-Vargas-Resume.pdf` / `Ana-Maria-Solis-Vargas-CV.pdf`. Accents and `ñ` are stripped from file names in both languages (the text of a Spanish CV keeps them). The suffix comes from `"resume"` in `template/strings.json`.
- `test` only runs the tests on the files already in the folder.
- Both write `test-report.md` in the output folder and print it (in UTF-8, also on a Windows console). **Exit code 0 only if the pre-checks and the 9 tests pass** (`Result: APPROVED — ready to deliver`). Anything else is `NOT APPROVED — do not deliver`.
- JSON inputs (`cv.json`, `snapshot.json`, the read files, the test 6 files) are read as UTF-8, with or without a BOM (Windows PowerShell 5 writes one).

### Try it with the example

The shipped output already has everything, including the two test 6 AI result files, so the honest check is to **copy it to a scratch folder inside the project and test the copy** (`my-data/reads/example-check/` in cv-factory, `mis-datos/lecturas/example-check/` in buscador-de-trabajo; the commands below use the first one). It must say `APPROVED — ready to deliver`. Never write into `engine/example/output/` during a check: it is the reference result.

English:

```
# macOS / Linux
mkdir -p my-data/reads/example-check/en
cp engine/example/output/*.* my-data/reads/example-check/en/
engine/.venv/bin/python engine/scripts/cv.py test engine/example/cv-example.json --snapshot engine/example/snapshot-example.json --out my-data/reads/example-check/en
```

```
# Windows (PowerShell)
New-Item -ItemType Directory -Force my-data\reads\example-check\en
Copy-Item engine\example\output\*.* my-data\reads\example-check\en\
engine\.venv\Scripts\python.exe engine\scripts\cv.py test engine\example\cv-example.json --snapshot engine\example\snapshot-example.json --out my-data\reads\example-check\en
```

Spanish (only where the project allows Spanish CVs, see `project.json` below):

```
# macOS / Linux
mkdir -p my-data/reads/example-check/es
cp engine/example/output/es/* my-data/reads/example-check/es/
engine/.venv/bin/python engine/scripts/cv.py test engine/example/cv-example-es.json --snapshot engine/example/snapshot-example.json --out my-data/reads/example-check/es
```

```
# Windows (PowerShell)
New-Item -ItemType Directory -Force my-data\reads\example-check\es
Copy-Item engine\example\output\es\* my-data\reads\example-check\es\
engine\.venv\Scripts\python.exe engine\scripts\cv.py test engine\example\cv-example-es.json --snapshot engine\example\snapshot-example.json --out my-data\reads\example-check\es
```

`generate` into a new, empty folder is expected to fail test 6 (`missing ai-from-pdf.json`): a new PDF needs two new agents with no context to read it and write their files (step 5 below). Only after they do does `cv.py test` say `APPROVED`. That is how it works for every real CV, too.

## How a CV is made

1. **Read the source data live and completely (every time).** All rows of the experience, achievements and skills databases, also the unverified ones (they do not go into the CV, but they say what to ask). Every page opened, not just its columns. Also the other hub pages (such as search preferences). Save each database as `experience.json`, `achievements.json` and `skills.json` and build the snapshot with `build_snapshot.py --hub-read` (pass the flag only if the hub, or `profile.json` for a spreadsheet source, was read in this same reading). If a row is missing, a page was not opened or the hub was not read, the engine stops.
2. **Compare with the job posting and ask.** Ask the person, one question at a time, when the posting asks for something that is not in the data but they might have, when something is ambiguous, or when something is not verified. Whatever they confirm is added to the source before using it, and the source is read again. Nothing is invented or assumed.
3. **Write `cv.json`** for the posting, with `sources` on every claim.
4. **Generate** with `cv.py generate`.
5. **Test 6:** start two agents with no context and send each one only the "Prompt to send" block of `scripts/tests/t6_instructions.md`, with the file to read (the PDF for one, `plain-text.txt` for the other) and the path to write (`ai-from-pdf.json` and `ai-from-text.json` in the output folder). Do not tell them about the tests or how the result is graded.
6. **Test** with `cv.py test`.
7. **Deliver only if it says `APPROVED — ready to deliver`.** Otherwise, fix and go back to step 4.

## The tests (pre-checks + 9)

- **Pre-check — data:** required fields present, only allowed characters, valid dates, and the CV language allowed by the project (see `project.json` below).
- **Pre-check — traceability:** the source was read completely (row counts match, every page opened, hub read, that is `build_snapshot.py --hub-read`); every claim lists its `sources`; every source exists; every achievement used is verified; the summary and bullets come from experience or achievement rows.
- **1** Fonts embedded, with a Unicode map, no Type 3, all Carlito (`pdffonts`).
- **2** Four readers (pdftotext, pdfminer, pdf.js, pdfium) recover at least 99.5 % of the words, with no forbidden characters.
- **3** No spaced-out letters and no words split with a hyphen at the end of a line.
- **4** Reading order: sections in order, contact details in the first 5 lines, title–company–dates together.
- **5** The open-source OpenResume parser extracts name, email, jobs and education.
- **6** Two AI agents with no context copy name, contact, jobs, dates, education and languages correctly.
- **7** Title, author and language in the metadata, under 1 MB, at most 2 pages, file name `First-Last-Resume` (English) or `First-Last-CV` (Spanish), with every part of the name and no accents.
- **8** The DOCX has no tables, text boxes or text in headers or footers; its text matches through two paths; converted to PDF with LibreOffice it passes tests 1 to 4.
- **9** English CV: no accented letters or ñ in the PDF, the DOCX, the metadata or the file name ("San Jose", "Tecnologico", also in proper names). The engine strips them itself; this test confirms none is left. It does not apply to Spanish CVs.

**Scope of test 5.** OpenResume is built for US resumes: it drops names with accents and only recognizes US phone numbers. English CVs have no accents; for a Spanish CV the test compares without accents, and it checks only name and contact, because OpenResume finds jobs and education by their English section titles; in Spanish CVs, jobs and education are verified by tests 4 and 6. If the phone is not a US number, that is noted and tests 4 and 6 cover it. In English CVs, OpenResume only recognizes an education entry by its own English keywords (school: `College`, `University`, `Institute`, `School`, `Academy`, `BASIS`, `Magnet`; degree: `Associate`, `Bachelor`, `Master`, `PhD`, `Ph.` or an abbreviation such as `AA`, `B.S.`, `MBA`; case-sensitive, as in its `extract-education.ts`). If neither the institution nor the degree of an entry has one, test 5 does not fail: it notes that OpenResume does not recognize it, and tests 4 and 6 verify it. Institution names are written only in their original official name, never translated: "Servicio Nacional de Aprendizaje" has no keyword (noted); "Bachelor's Degree in Business Administration, Universidad de Costa Rica" has a degree keyword (it must be extracted). An entry with a keyword still fails if OpenResume misses it. Adding a translation such as "(University of Costa Rica)" puts a school keyword and a degree keyword on the same line, and then OpenResume extracts nothing: one more reason not to translate institution names. Because of OpenResume, months are always written in full ("January 2021"): it does not recognize "Jan".

## Data formats

### cv.json

```
{
  "language": "en" | "es",
  "paper": "letter" | "a4",
  "job": {"company", "title", "link"},
  "contact": {"name", "headline", "location", "phone", "email", "linkedin", "portfolio"},
  "summary": {"text", "sources"},
  "skills": [{"category", "items": [...], "sources"}],
  "experience": [{"title", "company", "location", "start", "end", "sources", "bullets": [{"text", "sources"}]}],
  "projects": [{"name", "detail", "start", "end", "sources", "bullets"}],
  "education": [{"degree", "institution", "location", "start", "end", "sources", "bullets"}],
  "certifications": [{"name", "issuer", "start", "expires", "sources"}],
  "languages": [{"language", "level", "sources"}]
}
```

- Required in `contact`: `name`, `headline`, `location`, `email`. Every other section is optional.
- Dates: `"YYYY-MM"`, `"present"` or `"in_progress"`. They are written as full month names ("October 2025", "octubre 2025").
- Education and certifications may also use a year alone, `"YYYY"`, printed as just the year ("2018"), when the person only knows the year. Jobs and projects always need month and year: a year alone fails the pre-check ("jobs need month and year; ask the person").
- `paper`: `"letter"` or `"a4"` (default `"letter"`). Use `letter` for employers in the US, Canada, Mexico, Central America, Colombia, Venezuela and the Philippines, and `a4` everywhere else (the rest of South America, Spain, Europe). If unsure and the employer is a US company, `letter`.
- `languages`: the template prints `Language (level)`, so `level` is a plain phrase without parentheses, for example `"Native"`, `"C1, advanced"` / `"Nativo"`, `"B1, intermedio"`.
- `sources` is a list of snapshot row ids. The summary and every bullet must point to experience or achievement rows.
- `job` is not printed; it records which posting the CV is for.
- See `example/cv-example.json`.

### snapshot.json

```
{"read_at": "YYYY-MM-DD HH:MM",
 "note": "optional",
 "completeness": {"hub_read": true,
                  "databases": {"experience": {"rows_in_source": N},
                                "achievements": {"rows_in_source": N},
                                "skills": {"rows_in_source": N}}},
 "rows": {"<id>": {"database": "experience" | "achievements" | "skills",
                   "url": "...", "text": "...", "content": "<the page itself, may be empty>",
                   "verified": true | false | null}}}
```

Every row of every database goes in, each with `content` (a string, even if empty). Achievements count only when `verified` is `true`. See `example/snapshot-example.json`.

### build_snapshot.py

```
<PY> engine/scripts/build_snapshot.py <read-folder> <out/snapshot.json> --schema <schema.json> --hub-read
```

`--hub-read` means "the hub page and its other pages (Notion), or `profile.json` (spreadsheet source), were read in this same reading". It sets `completeness.hub_read`; without it, `hub_read` is `false` and the traceability pre-check fails, as it does whenever the hub was not read. Never pass it without reading the hub.

The read folder holds `experience.json`, `achievements.json` and `skills.json`, each one:

```
{"database": "...", "rows_in_source": N, "rows": [{"url": "...", "properties": {...}, "content": "..."}]}
```

`schema.json` says which properties make up each row's `text` (joined with ` | `, empty ones skipped) and which property marks an achievement as verified (value `"__YES__"`):

```
{"experience":   {"text_fields": ["Name", "English title", "Organization", "date:Period:start", "date:Period:end", "Summary"], "verified_field": null},
 "achievements": {"text_fields": ["Description", "English version", "Metric / result"], "verified_field": "Verified"},
 "skills":       {"text_fields": ["Skill", "Level", "Notes"], "verified_field": null}}
```

Row ids are stable between readings: the database letter (`E`, `A`, `S`) plus the last 6 characters of the page id in the `url`. A row with no `url` but an explicit `"id"` (for spreadsheet sources) keeps that id as-is. Duplicate ids stop the script.

### Spreadsheet source

For people who do not use Notion, the same data can live in one Excel workbook (`.xlsx`, it also opens in LibreOffice and Google Sheets). A spec file describes its tables, columns, drop-down options, checkbox labels and the instructions sheet. It is passed by path: `setup/workspace/workbook-spec.json` in cv-factory, or `configuracion/espacio/workbook-spec.json` in buscador-de-trabajo.

```
<PY> engine/scripts/workbook.py create <spec.json> <out.xlsx>                 # empty workbook to fill
<PY> engine/scripts/workbook.py schema <spec.json> <schema.json>              # schema for build_snapshot.py
<PY> engine/scripts/workbook.py upsert <spec.json> <file.xlsx> <rows.json>    # add or update rows
<PY> engine/scripts/workbook.py read   <spec.json> <file.xlsx> <read-folder>  # instead of reading Notion
<PY> engine/scripts/build_snapshot.py <read-folder> <out/snapshot.json> --schema <schema.json> --hub-read
```

- `create`: an instructions sheet first, then one sheet per table (experience, achievements, skills, target roles, applications, finder sources). The `ID` column comes first; the header row is bold, frozen and has filters; select and checkbox columns have drop-down lists, and each column title has a note.
- `read`: writes `experience.json`, `achievements.json` and `skills.json` with an explicit `"id"` per row (the `ID` cell, such as `E1`, `A3`, `S2`), so `cv.json` cites those IDs. `rows_in_source` is the number of rows with data. Every column goes into `properties` as text (checkboxes as `"__YES__"`/`"__NO__"`, dates as `YYYY-MM-DD`); `content` is the table's `content_column` (for example `Summary` or `Notes`). It stops with a clear message on a row with data but no ID, a duplicate ID, an ID without the table's prefix, a renamed or missing column, or a checkbox that is not one of the two labels. A row with only an ID is treated as empty.
- `upsert`: adds or updates rows without writing any spreadsheet code. `rows.json` maps a table key of the spec to a list of rows, each with its ID and only the columns to write, using the column names of the spec:

  ```
  {"achievements": [{"ID": "A7", "Description": "Trained 12 new hires", "Verified": "Yes"},
                    {"ID": "A2", "Metric / result": "15% less rework"}],
   "applications": [{"ID": "J4", "Status": "Applied", "Date applied": "2026-10-13"}]}
  ```

  A row whose ID is already in the sheet gets only the given columns changed; a new ID goes into the first empty row. Checkbox columns take `true`/`false`, `"yes"`/`"no"` or the spec's labels and are written as the labels (`Yes`/`No`, `Sí`/`No`); date columns take `"YYYY-MM-DD"` or `"YYYY-MM"` (written as real dates, the 1st of the month for `YYYY-MM`, shown as `yyyy-mm-dd`); number columns take numbers; select columns take one of their options; everything else is text; `null` or `""` empties a cell. Everything is checked before writing (unknown table or column, an ID without the table's prefix, a select value that is not an option, a bad date or number, an ID repeated in the input, the workbook open in Excel or LibreOffice) and, if anything is wrong, nothing is written. Drop-down lists, notes and formatting are kept. It prints one line per table, such as `Achievements & Responsibilities: 2 updated, 3 added`.
- `schema`: the `text_fields` and `verified_field` of the three inventory tables, taken from the spec.

Only achievements with the verified column set to the spec's "yes" label (`Yes`, `Sí`) can be used in a CV, exactly as with Notion.

### Test 6 result files

`ai-from-pdf.json` and `ai-from-text.json`, written by the two agents, with the schema in `scripts/tests/t6_instructions.md`.

### project.json (optional)

If the project root (the folder that contains `engine/`) has a `project.json` with `"cv_languages": ["en"]` (for example), a `cv.json` in any other language fails the pre-check. Without the file, `en` and `es` are both allowed.

## Integrity

`MANIFEST.sha256` lists the sha256 of every engine file of the release (except `.venv/`, `.node/`, `__pycache__/`, `*.pyc`, `.DS_Store`, `example/output/` and the manifest itself). Paths are written with `/` on every system. Text files are hashed with their line endings turned into LF, so a Git checkout on Windows that writes CRLF does not raise a false alarm; fonts, PDFs, DOCX, images and workbooks are hashed byte for byte.

```
<PY> engine/scripts/integrity.py --check   # warns about modified, added or deleted files; always exits 0
<PY> engine/scripts/integrity.py --write   # release step only: rewrites the manifest
```

`setup.py` runs `--check` and prints the result. A changed core file does not block anything, but CVs may then fail the tests; restore the original files from the release if that happens.
