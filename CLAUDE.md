<!-- Copyright 2026 Johel Gomez Rojas. Part of CV Factory. Licensed under the Apache License, Version 2.0 (see LICENSE and NOTICE). Do not remove this notice. -->

# CLAUDE.md — instructions for the AI (CV Factory)

> This file is for the AI agent. People start with `README.md`. Other agents (Codex, Gemini, Cursor…) read `AGENTS.md`, which points here.

CV Factory turns a person's verified career history into English CVs tailored to each vacancy, checked by 9 automated tests, and keeps a tracker of applications. An optional daily finder looks for vacancies in the cloud. **The person reviews and applies; the AI never applies.**

This project makes **English CVs only** (`project.json` → `cv_languages`). If a vacancy is in another language, say so and offer an English CV only if the vacancy accepts one.

## Running the engine (macOS, Linux, Windows)

| | macOS / Linux | Windows |
|---|---|---|
| **Setup** (with the system Python 3.10+) | `python3 engine/setup.py` | `py engine\setup.py` (or `python engine\setup.py`) |
| **`<PY>`**, the engine's Python | `engine/.venv/bin/python` | `engine\.venv\Scripts\python.exe` |

- Every engine command below is written as `<PY> engine/scripts/...`: replace `<PY>` with this machine's value. The setup prints it at the end (`Run the engine with: ...`). Run everything from the project folder.
- Forward slashes in the other paths work on Windows too. In Git Bash (Claude Code on Windows), write `<PY>` as `engine/.venv/Scripts/python.exe`.
- Folders and copies: use your file tools, or `mkdir -p` / `cp` (macOS, Linux, Git Bash), or `New-Item -ItemType Directory -Force` / `Copy-Item` (PowerShell).
- Windows: a program installed during the conversation is only in the PATH of a new terminal (the engine also looks in the usual install folders, so it usually finds it anyway). If poppler was unzipped by hand, the folder with `pdftotext.exe` goes in the `CVF_POPPLER_BIN` environment variable (`engine/README.md`).
- The person does not type these commands: you run them.

## At the start of every conversation

1. Read `my-data/profile.json`. **If it does not exist, or `onboarding.completed` is false, run `setup/onboarding.md`** from the first pending step. Nothing else happens before the onboarding is complete (except answering questions about the project).
2. Run the setup (`python3 engine/setup.py`, or `py engine\setup.py` on Windows) once per conversation before generating anything. It must end with `READY`. If it prints an integrity WARNING, tell the person in one line which core files changed and that CVs may fail because of it (do not fix or revert anything without their OK).
3. Storage is `notion` or `excel` (`profile.json` → `storage`). Use the matching branch below. With Excel, `profile.json` plays the role of the Notion hub (contact details, search preferences, history notes).

## How to talk to the person

- Plain words, short answers. **Questions in the chat, one at a time.** No multiple-choice boxes.
- Before big changes (to rules, to Notion structure, to files outside `my-data/` and `CVs/`), explain and wait for an OK.
- Never commit, push or merge without explicit permission each time.

## Where everything lives

| Path | What it is |
|---|---|
| `engine/` | The CV engine: template, scripts and the 9 tests. **Core files: do not modify** (see "Expand, don't modify") |
| `setup/` | Onboarding, Notion blueprint, finder rules and prompt, LinkedIn guide, workbook spec, profile template |
| `docs/` | User guide, how it works, expanding safely, and the research behind every rule (`docs/research/`) |
| `my-data/` | The person's private data: `profile.json`, `history/`, `reads/` (working folders, one per vacancy), and for Excel users `career-workbook.xlsx`, `finder-rules.md` and `linkedin-texts.md`. Never committed |
| `CVs/` | One folder per vacancy, with the delivered CV. Never committed |

## Writing to the Excel workbook

With Excel, **every write goes through the engine** (never edit the `.xlsx` with openpyxl or any other tool):

`<PY> engine/scripts/workbook.py upsert setup/workspace/workbook-spec.json my-data/career-workbook.xlsx <rows.json>`

`rows.json` = `{"<table key from the spec>": [{"ID": "J7", "<column>": value, ...}]}`, for example `{"applications": [{"ID": "J7", "Status": "CV ready", "Fit %": 85}]}`. The table keys are `experience`, `achievements`, `skills`, `target_roles`, `applications` and `finder_sources`; column names are exactly the spec's. An existing ID is updated (only the columns given); a new ID is appended (use the next free one: `J1`, `J2`…). The script validates everything first and writes nothing if a row is wrong; dates go as `YYYY-MM-DD`. Keep the `rows.json` in the working folder (or `my-data/reads/`). Ask the person to close the workbook in Excel before writing, so their open copy does not overwrite the change.

## With each vacancy (fixed steps)

The person pastes the **link and the job description** (in a new conversation, ideally). In batch ("make the CVs for the ones I marked"): read the Application Tracker, take every vacancy with Status = "Will apply" and do this for each, highest Fit % first.

**Working folder.** Each vacancy gets its own folder: `my-data/reads/<YYYY-MM-DD>-<company>/` (today's date and the company in lowercase with hyphens, e.g. `my-data/reads/2026-10-13-example-health/`); in the steps below, `<work>` means that folder. It holds the read JSONs (`experience.json`, `achievements.json`, `skills.json`), `snapshot.json`, `cv.json`, and `out/`, which is the engine's `--out`. Generation and tests run there; only an approved CV is copied to `CVs/` (step 11).

1. **Read the vacancy.** If there is a link, open it with WebFetch. LinkedIn, Indeed, Computrabajo, Remotive and other sites that block robots are never read by other means: ask the person to paste the text. **If there is no link** (only pasted text), ask where and when they saw it; in the tracker, Link = "pasted, no link" and Notes say "confirm it is still open".
2. **Eligibility and ghost check:** it must be doable from the person's country (`profile.json`), and not old, closed, a talent pool or a scam. If it fails, say why and stop (the person may still ask to continue).
3. **Read the whole inventory, live:** Experience & Education, Achievements & Responsibilities and Skills, every row (verified or not: the unverified ones tell you what to ask), **plus the hub (Notion) or `profile.json` (Excel)** in the same reading: contact details, search preferences and history notes. Pass `--hub-read` to `build_snapshot.py` only after reading it; without the flag the pre-check fails.
   - **Notion:** read each database **in view mode, never SQL or rows mode** (`notion-query-data-sources`, `"mode": "view"`, its Default view from `profile.json`, `page_size` 100, follow `next_cursor` until `has_more` is false). Open every row page (fetch) for its body. Use 3 subagents in parallel, one per database, each writing `<work>/experience.json`, `achievements.json`, `skills.json` as `{"database", "rows_in_source", "rows": [{"url", "properties", "content"}]}` where `rows_in_source` = every row the view returned and `content` = the page body (empty string if none). Read the hub page yourself. Then:
     `<PY> engine/scripts/build_snapshot.py my-data/reads/<YYYY-MM-DD>-<company> my-data/reads/<YYYY-MM-DD>-<company>/snapshot.json --schema setup/workspace/notion-snapshot-schema.json --hub-read`
   - **Excel:** read `my-data/profile.json` (the hub), then:
     `<PY> engine/scripts/workbook.py schema setup/workspace/workbook-spec.json my-data/reads/workbook-schema.json`
     `<PY> engine/scripts/workbook.py read setup/workspace/workbook-spec.json my-data/career-workbook.xlsx my-data/reads/<YYYY-MM-DD>-<company>`
     `<PY> engine/scripts/build_snapshot.py my-data/reads/<YYYY-MM-DD>-<company> my-data/reads/<YYYY-MM-DD>-<company>/snapshot.json --schema my-data/reads/workbook-schema.json --hub-read`
4. **Match, requirement by requirement:** show a table with each requirement, the evidence from the inventory, and the gap; then the Fit %. Required items weigh double; a requirement that is **partly met counts half** of its weight; Fit % = weight met / total weight, rounded to 5 %. If the person lacks experience in the role's main area but meets its functions: cap at 70 %, do not discard. Report the fit and gaps honestly, but **do not decide for the person** whether to apply.
5. **Ask, one question at a time,** about what the vacancy asks and the person might have but is not in the inventory, about anything ambiguous, and about anything not verified that would help. What they confirm is saved in the inventory first (achievements with Verified checked only when they confirm the exact wording; Excel: with `workbook.py upsert`). Then read the inventory again (step 3).
6. **Build `<work>/cv.json`** (format: `engine/README.md` and `engine/example/cv-example.json`) with `sources` on every claim, following the CV rules below. Where things live in the inventory: **languages** are Skills rows with Category "Language" (Level, e.g. "Native", and the CEFR level in Notes); **education and certifications** are Experience & Education rows with Type "Education" or "Certification". Dates: jobs and projects need `YYYY-MM` (if the month is missing, ask the person for it); education and certifications may be year only (`YYYY`).
7. **Generate:** `<PY> engine/scripts/cv.py generate my-data/reads/<YYYY-MM-DD>-<company>/cv.json --snapshot my-data/reads/<YYYY-MM-DD>-<company>/snapshot.json --out my-data/reads/<YYYY-MM-DD>-<company>/out`.
8. **Test 6:** two subagents **with no context**. Send each one **only the block "Prompt to send (copy only this block)" of `engine/scripts/tests/t6_instructions.md`**, plus the path of its input file and the path of the JSON to write: one gets `<work>/out/First-Last-Resume.pdf` and writes `<work>/out/ai-from-pdf.json`; the other gets `<work>/out/plain-text.txt` and writes `<work>/out/ai-from-text.json`. Never send them the grading section ("For the main agent only"), the cv.json or anything about the person. (Without subagents: two fresh model calls with no history. If that is impossible, test 6 fails and the CV is not delivered.)
9. **Test:** `<PY> engine/scripts/cv.py test my-data/reads/<YYYY-MM-DD>-<company>/cv.json --snapshot my-data/reads/<YYYY-MM-DD>-<company>/snapshot.json --out my-data/reads/<YYYY-MM-DD>-<company>/out` until it says `APPROVED`. If it fails, fix and go back to step 7. **Never deliver a CV that did not pass all 9 tests.** Education and Experience are never dropped to make a test pass: if a test fails because of how an entry is written, stop and tell the person what failed instead of removing content.
10. **Look at the PDF** (render the pages to images, e.g. `pdftoppm -png`, and check them).
11. **Save** (only after `APPROVED`) in `CVs/<Company - Short role>/`: at the top only the PDF and the DOCX from `<work>/out/`; in `details/`: `test-report.md`, `plain-text.txt`, `ai-from-pdf.json` and `ai-from-text.json` (from `<work>/out/`) and `cv.json` and `snapshot.json` (from `<work>`). The `.html` is not kept. The files keep the engine's names, without the company: `First-Last-Resume.pdf` / `.docx` (accents stripped, every part of the name kept, e.g. `Ana-Maria-Solis-Vargas-Resume.pdf`).
    **Folder name:** about 30 characters at most, no date. Shorten the company first (drop "Inc.", "LLC", "S.A.", "Support", "Group" and similar), then the role to its core or a common abbreviation, without levels or filler. Examples: "Example Health Group Inc." + "Claims Operations Coordinator III" → `Example Health - Claims Coordinator`; "Acme Support Services" + "Senior Quality Assurance Analyst" → `Acme - QA Analyst`. If the folder exists, add the month: `Example Health - Claims Coordinator (Nov)`.
12. **Record it in the Application Tracker** (Notion, or the workbook with `workbook.py upsert`): create or update the row with Status "CV ready", Link, Company, Fit % (**Notion: a number from 0 to 1, 0.8 = 80 %; Excel: from 0 to 100**), Gaps vs job post, Work mode, Work type (Back office, Calls, Mixed or Unconfirmed; **"Unconfirmed" unless the vacancy says**), Eligible from my country and Notes (why it fits, the CV folder, "passed the 9 tests"). Gaps and anything learned about the vacancy go in this row (with Excel there is no Learning Log or Research sheet).
13. **Show the CV** to the person (send the file if the tool allows, otherwise give the path) and sum up the decisions in a few lines.
14. **When they say they applied:** Status "Applied", Date applied = today, Next follow-up = today + 7 days, and the salary if they entered one. Remind them to check the application form fields (some portals fill them wrong from the CV).

## CV rules (summary; full version with sources: `docs/research/cv-rules.md`)

- **Never invent.** Every sentence comes from an inventory row; achievements only if Verified. The engine's pre-check rejects anything else.
- **CV headline = the exact title of the vacancy**, even when the fit is low. Job titles in Experience are never changed (use the official title or its English equivalent from the inventory). Summary and bullets only say what is verified.
- **English only, no accents or ñ** (the engine strips them: "San Jose"). **Proper names are never translated:** institutions (schools, colleges, universities) go only with their original official name, with no translation in parentheses: "Bachelor's Degree in Business Administration, Universidad de Costa Rica". Company names are never translated either.
- **Contact** from `profile.json`: name | phone | email | LinkedIn | City, Country. Never a full address, never a place listed in `person.never_show`.
- **Full month names** ("January 2021").
- **Paper size** (`cv.json` → `paper`): `letter` for employers in the US, Canada, Mexico, Central America, Colombia, Venezuela and the Philippines; `a4` elsewhere (the rest of South America, Spain, Europe). If unsure and the employer is in the US, `letter`.
- **Languages line:** the CV prints "Language (level)", so the level is a plain phrase without parentheses: "Native", "C1, advanced" → "English (C1, advanced)".
- **The same employer in two separate periods = two entries,** never one continuous range.
- **Old or less relevant jobs stay** (ATS compute years of experience from dates) with one bullet.
- **Projects** only if the vacancy asks for something the project proves.
- **Two pages at most.** Order: summary, skills, experience, (projects), education, certifications, languages. Education and Experience are never removed to pass a test.
- **Technical honesty:** describe how the person really works (e.g. "built with AI-assisted development" if that is the truth); never present skills beyond what the inventory's Notes say.
- **No hidden text, prompt injection or keyword stuffing.**

## Daily finder

If `profile.json` → `finder.enabled`, a cloud task runs it with the rules in the Notion page Daily Finder Rules (`setup/finder/`). Never change its schedule, volume or rules without the person asking.

**Searches by hand (Excel, or whenever the person asks "look for vacancies").** With Excel there is no scheduled finder. At the end of the onboarding (step 10) a local copy of the rules is filled in at `my-data/finder-rules.md`. When the person asks for a search, follow that file by hand, with these differences from the Notion finder:
- **Read** the workbook instead of Notion: the inventory with `workbook.py read` (as in step 3) and the Target Roles, Finder Sources and Application Tracker sheets (read only).
- **Write** the vacancies that pass to the Application Tracker sheet, and new sources to the Finder Sources sheet, with `workbook.py upsert`. Status "To review", Fit % from 0 to 100, **Found by = "Me"** (the person asked for the search; "Daily finder" is only for the scheduled task), Source = the board or company, and Notes start with "AI search of <YYYY-MM-DD>".
- **No Finder Log:** summarize the run in the chat (added, best fit, discarded by reason, sources that failed).

A Notion user who asks for a search in the conversation gets the same treatment, writing to Notion: Found by = "Me", and the summary in the chat (the Finder Log is only for the scheduled runs).

## Expand, don't modify

- **Welcome:** new finder sources, new Notion views/pages/databases, new target roles, new docs, preferences and finder settings.
- **Not recommended:** changing anything in `engine/` (template, scripts, tests, fonts). `engine/MANIFEST.sha256` records the release; the setup warns if a file changed. If the person asks to change the engine, explain the risk (CVs may stop passing the tests) and do it only with their explicit OK. Never write into `engine/example/output/`.

## Never

Apply for the person, create accounts, write to recruiters or anyone, read LinkedIn or other sites that block robots by other means, invent or embellish experience, use unverified achievements, or deliver a CV that did not pass the 9 tests.
