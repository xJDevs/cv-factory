<!-- Copyright 2026 Johel Gomez Rojas. Part of CV Factory. Licensed under the Apache License, Version 2.0 (see LICENSE and NOTICE at the project root). Do not remove this notice. -->

# Onboarding (first-time setup)

The agent runs this the first time someone opens the project, and again whenever `my-data/profile.json` says a step is still pending. It turns an empty copy of CV Factory into the person's own: their data, their workspace, their finder.

## How to run it

- **Speak plainly, one question at a time, in the chat.** No multiple-choice boxes. Wait for the answer before the next question. Short messages.
- **Save progress after every step** in `my-data/profile.json` → `onboarding.completed_steps`: a list of step numbers as strings, in order, with a skipped step written as `"N-skipped"`, e.g. `["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10-skipped", "11"]` (also in `setup/profile-template.json` → `_help`). If the conversation ends, the next one continues where it stopped: say "Last time we finished step N; let's continue with …".
- **Never invent anything about the person.** Everything comes from what they give or confirm.
- **Before anything that writes outside the project folder** (creating Notion pages, a scheduled task, moving the folder), say what you will do and wait for an OK.
- **With Excel, every write to the workbook goes through `workbook.py upsert`** (see `AGENTS.md`, "Writing to the Excel workbook"); never edit the `.xlsx` with other tools.
- The whole onboarding can take one long conversation or several short ones. Step 7 (the inventory) is the longest; it can be split.

## Step 0 — Welcome and terms

1. **First, create the private folders** if they don't exist: `my-data/`, `my-data/history/`, `my-data/reads/` and `CVs/`, and `my-data/profile.json` as a copy of `setup/profile-template.json` **without its `_about` and `_help` keys**. Both `my-data/` and `CVs/` are private: they are in `.gitignore` and never leave the computer except through the person's own Notion. From here on, progress is saved in that file.
2. In three or four lines: what CV Factory does (career inventory → tailored English CVs that pass 9 tests → application tracker → optional daily finder) and what it never does (apply, create accounts, write to recruiters, invent experience).
3. Show the key points of `DISCLAIMER.md` in plain words:
   - **Only true information.** No CV is built from false data. If someone gives false information, that is their sole responsibility.
   - **Costs:** the AI usage (subscription or tokens) is the person's. The more work they give it (more vacancies, more sources, two finder runs a day), the more it uses. The author is not responsible for any usage or charges.
   - **No guarantees** of interviews or jobs; they review every CV before sending it.
   - **Respect each site's terms:** the project never reads LinkedIn or other sites that forbid robots.
   - **Expand, don't modify:** adding sources, databases or pages is welcome; changing `engine/` files is not recommended unless they know what they are doing (setup warns if a core file changed).
4. Ask them to confirm they accept. Without a clear yes, stop. Save `disclaimer_accepted` with today's date and `completed_steps` = `["0"]`.

## Step 1 — The folder and the agent project

1. Check where the project folder is. It should be on the Desktop and named **`cv-factory`**. Find the real Desktop of this computer first, because it is not always `~/Desktop`:
   - **macOS:** `~/Desktop/cv-factory`.
   - **Linux:** the folder `xdg-user-dir DESKTOP` prints (it may have another name in other languages); usually `~/Desktop`.
   - **Windows:** run `powershell -NoProfile -Command "[Environment]::GetFolderPath('Desktop')"` (it works from PowerShell and from Git Bash). It is often `C:\Users\<name>\Desktop`, but when OneDrive backs up the Desktop it is `C:\Users\<name>\OneDrive\Desktop` (or the Desktop folder's name in the system language, such as `Escritorio`). Use the path it prints. If the Desktop is in OneDrive, tell the person in one line that OneDrive will copy the folder, including their private `my-data/`, to their OneDrive account; if they prefer it not to, they can keep the folder somewhere OneDrive does not back up (for example `C:\Users\<name>\cv-factory`) and link that one instead.
2. Recommend, and explain how to, **create a project in their agent** (a Project in Claude, or the equivalent elsewhere):
   - instructions: "Read AGENTS.md in the linked folder and follow it" (the same for every agent);
   - the `cv-factory` folder on the Desktop linked or attached to it;
   - **one new conversation per CV**: each vacancy gets its own conversation inside that project. It keeps each CV clean and the context small.
3. If the folder is elsewhere or has another name, offer to move or rename it (ask first). **Before moving it, save step 1 as completed** in `profile.json` (it travels with the folder). Then move it (`mv` on macOS, Linux and Git Bash; `Move-Item` in PowerShell, with the Desktop path found above), and tell the person to reopen the agent on the new location (and link the new folder in the agent project). The engine's local folders (`engine/.venv`, `engine/.node`) move with it; the setup in step 2 checks them again. On Windows, close any program that has a file of the folder open first, or the move fails. The next conversation resumes from step 2.

## Step 2 — Model and tools

1. Recommend the **most capable model** they have (today Claude Opus 5.5 or its equivalent) for CVs and for the finder. Smaller models make more mistakes with eligibility, fit and the tests.
2. Run the setup: `python3 engine/setup.py` on macOS and Linux, `py engine\setup.py` (or `python engine\setup.py`) on Windows. It must end with `READY`; the line before it says which `<PY>` to use on this machine (see `AGENTS.md`, "Running the engine"). If something is missing, tell them exactly what to install, in plain words (the script prints the command), and run it again. What it usually means:
   - **Mac:** Homebrew (https://brew.sh), then `brew install python poppler node` and `brew install --cask libreoffice`.
   - **Linux:** `sudo apt install python3 python3-venv poppler-utils nodejs npm libreoffice-writer fonts-crosextra-carlito git`.
   - **Windows 10/11:** in PowerShell, `winget install -e --id Python.Python.3.13`, `winget install -e --id OpenJS.NodeJS.LTS`, `winget install -e --id oschwartz10612.Poppler`, `winget install -e --id TheDocumentFoundation.LibreOffice` and `winget install -e --id Git.Git` (**Claude Code on Windows needs Git for Windows**). Then close and reopen the terminal and the agent, so the new programs are found, and run the setup again. If winget cannot install poppler: download the latest zip of https://github.com/oschwartz10612/poppler-windows/releases, unzip it (for example in `C:\poppler`) and set `CVF_POPPLER_BIN` to the folder that has `pdftotext.exe` (`setx CVF_POPPLER_BIN "C:\poppler\poppler-<version>\Library\bin"`, then a new terminal). LibreOffice is found in `C:\Program Files\LibreOffice` without touching PATH.
3. **Check the engine on their machine with the example.** Copy the approved example to the reads folder and run the 9 tests on that copy (never write into `engine/example/output/`):
   ```
   # macOS / Linux (and Git Bash on Windows, with <PY> = engine/.venv/Scripts/python.exe)
   mkdir -p my-data/reads/example-check
   cp engine/example/output/*.* my-data/reads/example-check/
   engine/.venv/bin/python engine/scripts/cv.py test engine/example/cv-example.json --snapshot engine/example/snapshot-example.json --out my-data/reads/example-check
   ```
   ```
   # Windows (PowerShell)
   New-Item -ItemType Directory -Force my-data\reads\example-check
   Copy-Item engine\example\output\*.* my-data\reads\example-check\
   engine\.venv\Scripts\python.exe engine\scripts\cv.py test engine\example\cv-example.json --snapshot engine\example\snapshot-example.json --out my-data\reads\example-check
   ```
   It must say `APPROVED`. If it does not, show them the failing lines of `my-data/reads/example-check/test-report.md` and fix the setup before going on.

## Step 3 — Their career history

Ask what they have, best first:

1. **A document with their full history:** jobs, dates, responsibilities, achievements, numbers, tools. Ideal.
2. **Old CVs — ideally at least 5.** Each old CV usually has things the others don't. Also their **LinkedIn profile as a PDF** (on the profile: More → Save to PDF).
3. **Nothing written:** they tell it as it comes, typed or by voice, even if messy. Write it down for them in `my-data/history/history.md` and show it back.

Put every file they give you in `my-data/history/`. Read all of it. Then list **contradictions between sources** (dates, titles, numbers) to resolve in step 7. If they have an official record of their dates (social security or tax record, work certificates), it is the best source for dates.

## Step 4 — Where their data will live

Ask: **"Do you use Notion?"**

- **Yes** → step 5 with Notion.
- **No** → recommend it, clearly and with the reasons:
  - It is **free** for personal use.
  - **The daily finder runs in the cloud, even with the computer off.** To leave the vacancies it finds, it needs an online place to write. Notion is one; a file on the computer is not.
  - The AI reads the inventory live for every CV and saves there what the person confirms.
  - They can filter and sort the vacancies (by status, by fit, by calls vs back office), and see everything **on the phone**.
- If they still prefer not to: use **Excel** (one workbook, one sheet per table: `my-data/career-workbook.xlsx`). It works the same for CVs. The one difference, said clearly: **there is no automatic daily finder**; they ask for vacancies in a conversation ("look for vacancies for me") and the agent searches with the same rules.

Save `storage` = `notion` or `excel`.

**Connect Notion (if chosen).** The agent needs the official Notion MCP connector:
- Claude app / claude.ai: Settings → Connectors → Notion → connect and allow access to the workspace (all pages, or at least the page where CV Factory will live).
- Claude Code: the claude.ai connectors are available automatically after connecting them there; or add the server with `claude mcp add --transport http notion https://mcp.notion.com/mcp` and log in.
- Other agents: add the Notion MCP server (`https://mcp.notion.com/mcp`) in that tool's MCP settings.
Test it: search the workspace for any page. If it fails, help them fix it before going on.

## Step 5 — Build the workspace

- **Notion:** follow `setup/notion-workspace.md` exactly (hub, 9 databases in order, extra views, the three guide pages; the Daily Finder Rules and LinkedIn pages are filled in later, at steps 10 and 11). Save every URL, data source and Default view in `profile.json` → `notion`. Fetch everything at the end to verify.
- **Excel:** `<PY> engine/scripts/workbook.py create setup/workspace/workbook-spec.json my-data/career-workbook.xlsx`. Tell them they can open it, but should not rename sheets or columns. What changes with Excel:
  - `my-data/profile.json` is the hub: contact details, search preferences and history notes live there.
  - The workbook has the inventory, Target Roles, Application Tracker and Finder Sources sheets. **There is no Learning Log, Research or Finder Log sheet** (those exist only in Notion): gaps found for a vacancy are written in that vacancy's Application Tracker row, and a search is summarized in the chat.
  - The finder rules live in `my-data/finder-rules.md` (step 10) and the LinkedIn texts in `my-data/linkedin-texts.md` (step 11).

## Step 6 — Contact details and preferences

One question at a time:
1. Professional name exactly as it should appear on CVs and LinkedIn (English CVs drop accents automatically).
2. Phone (with country code), email, LinkedIn URL, portfolio or website if any.
3. City and country to show on CVs (city and country only; never a full address). Ask if there is a place name they never want shown (`person.never_show`).
4. Time zone (infer it from the country and confirm).
5. Work mode: remote, hybrid, on-site or any; from where; how far they would commute for on-site.
6. **Minimum acceptable salary** per month, in their currency, and the ideal. Vacancies that publish less than the minimum are discarded; vacancies with no salary still count.
7. What kind of roles interest them (`preferences.target_areas`, free text: it goes in the hub and guides the finder). Tell them not to limit themselves to their current title: step 8 proposes nearby roles too. This project searches and writes in English (`preferences.search_languages` = `["en"]`).
8. What kind of work they want or avoid (`preferences.job_types`, free text), e.g. "back office only, no call-center roles" or "calls are fine".
9. Their career areas (`tracks`), e.g. Claims, Operations, Data. They become the Track options of the Notion databases (with Excel they are only kept in `profile.json`). Propose them from the history and let them adjust.

Save everything in `profile.json`. **Notion only:** fill the hub (Search preferences, Contact details) with the hub template. With Excel, `profile.json` is the hub, so there is nothing else to fill.

## Step 7 — The career inventory (the most important step)

Turn the history into rows (Notion databases, or workbook sheets written with `workbook.py upsert`):

- **Experience & Education:** one row per position, degree, certification, course or project, with the official title, the English title, organization, exact period, location/work mode and a summary. A promotion is a new row. **Education and certifications** are rows here with Type "Education" or "Certification". Ask for each institution's and company's **official name** as it is written in its own language. It is never translated, not even in parentheses: CVs use only that name.
- **Achievements & Responsibilities:** one row per bullet, in the person's words (Description) plus the CV-ready English version, the metric, the context and the link to where it happened and which skills it shows.
- **Skills:** every skill, with level, years, synonyms and an honest note of its scope. **Languages** are Skills rows with Category "Language": Level "Native" for the mother tongue (otherwise Basic to Expert) and the CEFR level in Notes (e.g. "C1; EF SET certificate 2024").

Then **verify**, one question at a time:
- Resolve every contradiction found in step 3.
- For every achievement: show the English version and the number, ask "Is this exactly true?" Only when they confirm the wording, check **Verified**. Inflated numbers from old CVs: keep the most conservative one they confirm.
- Dates: month and year for every start and end of jobs and projects (the CV needs `YYYY-MM`). For education and certifications the year alone is enough.
- Things that are true but should not go in CVs (a one-week training, an unfinished degree): write them as history notes, each with the reason and the date it was decided. **Notion:** the hub's History notes section. **Excel:** `profile.json` → `history_notes`.

Do not rush this step. Every future CV can only use what is verified here. It is fine to verify the main jobs first and leave older ones for later; say what is still pending.

## Step 8 — Target roles

Cross the verified inventory with the market and propose **target roles**: their current role, similar roles, roles one level up, and roles in other areas where their experience overlaps. For each one: fit %, why it fits (citing the inventory), gaps and how to close them, equivalent titles (how other companies call it, in English) and a reference salary range if you can find a reliable one. If they lack experience in a role's main area but meet its functions, cap the fit at 70 % and say why. Let them set the priority (High / Medium / Low / Discarded). Write them in Target Roles (Fit %: from 0 to 1 in Notion, from 0 to 100 in Excel).

## Step 9 — Finder sources

1. From `setup/finder/sources-catalog.json`, propose the sources that fit them: global remote boards always; regional boards for their region; country boards for their country; never anything in `blocked`.
2. **Research companies** that hire people like them where they can work from (local offices, companies hiring remotely in their region for their target roles) and whose careers page or ATS can be read for free. Propose **3 to 5**, each with the reason. This can be skipped and done later ("research companies for me" in any conversation).
3. Add the web-search queries for sites that cannot be read (LinkedIn, Indeed and similar): those results always enter as "Finder (unverified)".
4. They approve the list; write it in Finder Sources (Notion) or **the Finder Sources sheet** (Excel), one row per source, Active checked, with:

   | Catalog `type` | Type option | Notes |
   |---|---|---|
   | `remote_board` | Remote board | |
   | `latam_board` | Remote board | Write the region in Why (e.g. "Latin America board") |
   | `country_board` | Local job board | |
   | `ats_api_pattern` | Company ATS API | One row per company, with URL or query filled from the pattern (e.g. the company slug in `{company}`) |
   | `web_search` | Web search | URL or query = the query; put the allowed domains in Notes |

   **Notes always start with "Has date: yes." / "Has date: no." / "Has date: relative."**, from the catalog's `has_posting_date` ("unknown" → "Has date: no."), followed by the catalog's useful notes. The midday run only uses "Has date: yes" sources.
5. Say that they can add companies any time, and that the finder adds new ones it finds on its own.

## Step 10 — The daily finder

**Notion** — follow `setup/finder/finder-prompt.md`:
1. **Volume:** 10 or 20 vacancies per run. Say it clearly: more vacancies, more sources and two runs a day mean more subscription or token use, and that is their responsibility.
2. **Fit:** minimum 75 % to enter, phone alert from 85 % (they can change both).
3. **Times:** recommend a full run early in their morning and a recheck at midday, converted to their time zone, and explain why (morning = full run before the day starts; midday = recheck after the US morning, when many remote roles are posted). They can choose other times.
4. **Model:** the most capable one.
5. Fill in and create the Notion page Daily Finder Rules (`setup/finder/finder-rules.md`). `{{EXTRA_BLOCKED_SITES}}` = the `blocked` entries of `setup/finder/sources-catalog.json` whose name or reason matches their country or region and that are not already in the list (or remove the placeholder).
6. With their OK, create the scheduled task, run it once, and check the Finder Log row and the vacancies it added together with them. If they do not want the finder, save the step as `"10-skipped"` and leave `finder.enabled` false.

**Excel** — there is no scheduled finder. Fill a local copy of `setup/finder/finder-rules.md` at `my-data/finder-rules.md` with their values (everything below the line; country, salary, fit and volume filled in; the run times removed). Then adapt it for searches by hand, as `AGENTS.md` ("Daily finder") says: every search uses the morning window (last 7 days); section 1 reads the workbook instead of Notion; section 6 writes to the Application Tracker sheet with `workbook.py upsert` (Found by = "Me", Fit % from 0 to 100); sections 7 and 8 become a summary in the chat (there is no Finder Log). Tell them: to search, they say "look for vacancies for me" in a conversation.

## Step 11 — LinkedIn

Generate the **LinkedIn — Texts** page following `setup/linkedin-guide.md`, starting from their current profile PDF if they gave one: in Notion, the guide page under the hub; with Excel, the file `my-data/linkedin-texts.md`. Remind them: they make every change by hand; the AI never touches LinkedIn.

## Step 12 — Ready

Explain, in a few lines:
- **To get a CV:** open a new conversation in the agent project and paste the vacancy's **link and job description**. The AI checks eligibility, shows the match, asks about gaps one question at a time, builds the CV, runs the 9 tests and saves it in `CVs/Company - Role/`.
- **In batch:** mark vacancies as "Will apply" in the Application Tracker and say "make the CVs for the ones I marked".
- **To search (Excel, or any time):** say "look for vacancies for me".
- **LinkedIn and other blocked sites:** they search by hand (the quick-search links help) and paste the job description; from there everything is the same.
- **After applying:** tell the AI ("I applied"), so it records the date and a follow-up in 7 days.

Mark the onboarding as completed in `profile.json` (`onboarding.completed` = true).
