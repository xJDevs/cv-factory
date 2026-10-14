<!-- Copyright 2026 Johel Gomez Rojas. Part of CV Factory. Licensed under the Apache License, Version 2.0 (see LICENSE and NOTICE at the project root). Do not remove this notice. -->

# Notion workspace: how to build it

This is the blueprint of the person's **CV Factory** workspace in Notion: one hub page, nine databases and three guide pages. The onboarding (`setup/onboarding.md`, step 5) builds it with the Notion MCP tools. Build it exactly as described here: the CV flow and the daily finder rely on these names.

`{{...}}` are filled in from `my-data/profile.json`. Never leave a placeholder in Notion: if a value is unknown, ask the person or leave the line out.

## Rules for the agent

- **Create everything under one new page** called **CV Factory** (icon 🏭) at the top level of the person's workspace, unless they name another parent.
- **Order matters** for the two-way relations: create the databases in the order below (a relation can only point to a database that already exists).
- `notion-create-database` adds each database at the end of the parent page. When everything exists, rewrite the hub with `notion-update-page` (`replace_content`) using the hub template below, so each database sits under its heading. Keep every `<database>` and `<page>` tag exactly as fetched; never delete one.
- **Read databases in view mode, never with SQL.** `notion-query-data-sources` with `"mode": "view"` on the database's **Default view**, `page_size` 100, following `next_cursor` until `has_more` is false. SQL and `rows` mode count against a Notion plan quota and stop working when it runs out; view mode does not. Never add filters to a Default view (create a separate view to filter).
- After building, **fetch every database** and save in `my-data/profile.json` → `notion`: the hub URL, and for each database its database URL, `collection://` data source and Default `view://` URL. The CV flow and the finder read those.
- Verify at the end: fetch the hub and check the order of headings, databases and pages; fetch each database and compare its properties with this file.

## Databases (create in this order)

### 1. Experience & Education

Every job, degree, certification, course, project or volunteer role. One row per position (a promotion inside one company = one row per title).

```sql
CREATE TABLE (
  "Name" TITLE COMMENT 'Job title, degree, certification or project, as officially held (never changed later)',
  "Type" SELECT('Job':blue, 'Freelance/Own business':green, 'Own project':pink, 'Education':yellow, 'Certification':purple, 'Course':gray, 'Volunteering':brown),
  "Organization" RICH_TEXT,
  "English title" RICH_TEXT COMMENT 'Official or equivalent English title for international CVs',
  "Period" DATE,
  "Current" CHECKBOX,
  "Location / work mode" RICH_TEXT,
  "Industry" RICH_TEXT,
  "Summary" RICH_TEXT COMMENT 'What the role really was, clarifications the person confirmed, source of the dates, and "To complete: ..." for missing data',
  "Link / credential" URL
)
```

`Period` holds start and end (end empty and `Current` checked for the current role). The relation to achievements is added by database 3.

### 2. Skills

```sql
CREATE TABLE (
  "Skill" TITLE,
  "Category" SELECT('Technical':blue, 'Tool/Software':purple, 'Domain/Industry':orange, 'Soft':green, 'Language':yellow, 'Certifiable':pink),
  "Level" SELECT('Basic':gray, 'Intermediate':yellow, 'Advanced':green, 'Expert':blue, 'Native':purple),
  "Years of use" NUMBER,
  "Last used" DATE,
  "Synonyms / how job posts ask for it" RICH_TEXT COMMENT 'Other ways it appears in job descriptions, for matching',
  "Track" MULTI_SELECT({{TRACK_OPTIONS}}),
  "Notes" RICH_TEXT COMMENT 'Honest scope: what the person has and has NOT done with it'
)
```

**Languages** are Skills rows with Category `Language`: Level `Native` for the mother tongue (otherwise Basic to Expert) and the CEFR level in Notes (e.g. "C1"). Education and certifications are rows of Experience & Education with Type `Education` or `Certification`.

### 3. Achievements & Responsibilities

The bullets of the CV. **Only rows with `Verified` checked can appear in a CV.**

```sql
CREATE TABLE (
  "Description" TITLE COMMENT 'Base wording, one line, in the person''s own words',
  "Type" SELECT('Achievement':green, 'Responsibility':blue, 'Project':pink, 'Recognition':yellow),
  "Where" RELATION('{{DS_EXPERIENCE}}', DUAL 'Achievements & responsibilities'),
  "Skills shown" RELATION('{{DS_SKILLS}}', DUAL 'Evidence'),
  "Metric / result" RICH_TEXT COMMENT 'Numbers: %, time, volume, money, cases',
  "Context" RICH_TEXT COMMENT 'Situation and how it was done (STAR), for interview answers; where the number comes from',
  "English version" RICH_TEXT COMMENT 'CV-ready English bullet: action verb, no first person',
  "Track" MULTI_SELECT({{TRACK_OPTIONS}}),
  "Verified" CHECKBOX COMMENT 'The person confirmed it is accurate'
)
```

### 4. Application Tracker

Every vacancy, found by the finder or by the person. Created before Target Roles so the two-way relation can point to it.

```sql
CREATE TABLE (
  "Job" TITLE COMMENT 'Role — Company',
  "Status" SELECT('To review':gray, 'Will apply':yellow, 'CV ready':orange, 'Applied':blue, 'Interview':purple, 'Offer':green, 'Rejected':red, 'Discarded':default),
  "Company" RICH_TEXT,
  "Link" URL,
  "Source" SELECT('LinkedIn':blue, 'Company site':gray, 'Referral':pink, 'Other':default, 'Finder (unverified)':gray),
  "Found by" SELECT('Daily finder':blue, 'Me':green),
  "Work mode" SELECT('On-site (local)':green, 'Hybrid (local)':yellow, 'Remote (country/region)':blue, 'Remote (international)':purple),
  "Work type" SELECT('Back office':green, 'Calls':orange, 'Mixed':yellow, 'Unconfirmed':gray) COMMENT 'Back office = almost no calls (tickets, data, email). Calls = the phone is the core of the job. Mixed = both matter.',
  "Fit %" NUMBER FORMAT 'percent',
  "Gaps vs job post" RICH_TEXT,
  "Eligible from my country" RICH_TEXT COMMENT 'Quote from the posting that proves it can be done from {{COUNTRY}}',
  "Knockout questions" RICH_TEXT COMMENT 'Work authorization, salary, certifications, schedule, language',
  "Salary" RICH_TEXT,
  "Contact / referral" RICH_TEXT,
  "Notes" RICH_TEXT,
  "CV sent" FILES,
  "Date posted" DATE,
  "Date applied" DATE,
  "Next follow-up" DATE,
  "Found" CREATED_TIME
)
```

`Status` is a select (not a status property): the flows filter on these exact option names. The finder adds a `Source` option per job board the first time it uses one.

### 5. Target Roles

```sql
CREATE TABLE (
  "Role" TITLE COMMENT 'Role family, e.g. "Claims Specialist / Claims Analyst"',
  "Track" SELECT({{TRACK_OPTIONS}}),
  "Fit %" NUMBER FORMAT 'percent',
  "Priority" SELECT('High':red, 'Medium':yellow, 'Low':gray, 'Discarded':default),
  "Market" MULTI_SELECT('On-site/hybrid in {{COUNTRY}}':green, 'Remote {{COUNTRY}}/{{REGION}}':blue, 'Remote international':purple),
  "Equivalent titles" RICH_TEXT COMMENT 'How this role is called at other companies; the finder searches with Role + these',
  "Why it fits" RICH_TEXT,
  "Gaps" RICH_TEXT,
  "How to close the gap" RICH_TEXT,
  "Reference salary range" RICH_TEXT,
  "Key skills" RELATION('{{DS_SKILLS}}'),
  "Applications" RELATION('{{DS_APPLICATIONS}}', DUAL 'Target role')
)
```

### 6. Learning Log

New things the person learns or builds; feeds the inventory and LinkedIn.

```sql
CREATE TABLE (
  "What it was" TITLE,
  "Type" SELECT('Learned':blue, 'Built':pink, 'Certification/Course':purple, 'Work achievement':green, 'Post/Content':yellow),
  "Date" DATE,
  "Detail" RICH_TEXT,
  "Evidence (link)" URL,
  "Skills" RELATION('{{DS_SKILLS}}'),
  "LinkedIn draft" RICH_TEXT COMMENT 'Ready text: post, experience bullet or project entry',
  "LinkedIn" SELECT('Pending':gray, 'Draft ready':yellow, 'Added to profile':blue, 'Post published':green, 'Not applicable':default),
  "Moved to inventory" CHECKBOX
)
```

### 7. Research

Key findings about how hiring works (seeded from `docs/research/README.md`, one row per key point).

```sql
CREATE TABLE (
  "Finding" TITLE,
  "Topic" SELECT('Market and volume':gray, 'How ATS work':blue, 'AI agents':purple, 'CV format':green, 'What hurts':red, 'What works':yellow, 'LinkedIn':blue, '{{REGION}}':orange),
  "Confidence" SELECT('High':green, 'Medium':yellow, 'Vendor data':orange),
  "Source" URL,
  "Date of data" DATE,
  "What it means for CV Factory" RICH_TEXT,
  "Added" CREATED_TIME
)
```

### 8. Finder Sources

Where the daily finder looks. Filled at onboarding (`setup/finder/sources-catalog.json` + the person's own companies) and grown by the finder itself.

```sql
CREATE TABLE (
  "Source" TITLE,
  "Type" SELECT('Company ATS API':blue, 'Remote board':green, 'Web search':gray, 'Company career site':brown, 'Local job board':orange),
  "Active" CHECKBOX,
  "URL or query" RICH_TEXT COMMENT 'URL that is read (or the web search query)',
  "Why" RICH_TEXT,
  "Notes" RICH_TEXT COMMENT 'Start with "Has date: yes/no/relative." — the midday run only uses "Has date: yes"'
)
```

### 9. Finder Log

One row per finder run. The detail goes in the **body** of each row page (template in `setup/finder/finder-rules.md`, section 7).

```sql
CREATE TABLE (
  "Run" TITLE COMMENT 'Finder YYYY-MM-DD morning / Finder YYYY-MM-DD midday',
  "Date" DATE,
  "Sources checked" NUMBER,
  "Jobs seen" NUMBER,
  "Added" NUMBER,
  "Discarded" NUMBER,
  "Best fit" NUMBER FORMAT 'percent',
  "Summary" RICH_TEXT,
  "Problems" RICH_TEXT
)
```

`{{TRACK_OPTIONS}}` = the person's tracks (career areas) agreed at onboarding, e.g. `'Claims':orange, 'Operations':brown, 'Data':blue, 'Cross-functional':gray`. In Target Roles the last option is `'Hybrid':purple` instead of `'Cross-functional'`.

## Extra views

Create with `notion-create-view` (read `notion://docs/view-dsl-spec` first), then fetch to check:

- **Achievements & Responsibilities → "To verify"** (table): `FILTER "Verified" = false`, group by `Where` (hide empty groups), show Description, Verified, Metric / result, Context. If grouping by a relation is not accepted, keep the filter and skip the grouping.
- **Application Tracker → "Pipeline"** (board): `GROUP BY "Status"`, `SORT BY "Found" DESC`, show Job.
- **Application Tracker → Default view**: `SORT BY "Found" DESC` (sort only, no filter).
- **Research → "By topic"** (table): `GROUP BY "Topic"`.

## Hub page template

Title **CV Factory**, icon 🏭. Replace `<database>` / `<page>` URLs with the real ones.

```markdown
<callout icon="🎯" color="blue_bg">
	A system to shorten the time between finding a vacancy and sending a CV made for it. **It never applies on its own**: the AI prepares, {{FIRST_NAME}} reviews and sends.
</callout>
## How it works
1. **Career inventory**: everything I have done (jobs, responsibilities, achievements, skills), before thinking about any job.
2. **Target roles**: the AI crosses the inventory with the market and proposes roles that fit, with fit % and gaps.
3. **Tailored CV**: I paste a job description and its link → requirement-by-requirement match → questions about gaps → CV in PDF and DOCX that passes 9 tests.
4. **Daily finder**: a scheduled task (every day at {{RUN_TIME_MORNING}} and {{RUN_TIME_MIDDAY}}, the midday one lighter) that looks for vacancies and leaves up to {{MAX_PER_RUN}} per run, with a fit of {{MIN_FIT_PERCENT}} % or more, in the Application Tracker. It follows *Daily Finder Rules*, reads *Finder Sources* and writes one row per run in *Finder Log*.
5. **LinkedIn**: the *LinkedIn — Texts* page has the profile ready to copy, and the *Learning Log* keeps it growing.
## Search preferences
- **Work mode:** {{WORK_MODE_PREFERENCE}}
- **Where:** {{WHERE_PREFERENCE}}
- **What:** {{TARGET_AREAS}}. Any role where my experience overlaps, even if the fit is not 100 %, always with the % and what is missing.
- **Minimum salary:** {{SALARY_MIN}} per month (vacancies that publish less are discarded; those without a salary still count).
<callout icon="📂" color="gray_bg">
	The CVs, the engine and the full research live in the **{{LOCAL_FOLDER_NAME}}** folder on my computer's Desktop.
</callout>
## Contact details (for CVs)
- **Professional name:** {{FULL_NAME}}
- **Phone:** {{PHONE}}
- **Email:** [{{EMAIL}}](mailto:{{EMAIL}})
- **LinkedIn:** [{{LINKEDIN_URL}}](https://{{LINKEDIN_URL}})
- **Location:** {{CITY}}, {{COUNTRY}}
## History notes
- Things that are true but must not appear in CVs (short trainings, unfinished degrees, courses not to use), each with the reason and the date it was decided.
## Golden rule
Nothing is ever invented. Tailoring = choosing, reordering and rewording what is already in the inventory. If evidence is missing, it is marked as a gap.
---
## 📦 Career inventory
<database url="{{DB_EXPERIENCE}}">Experience & Education</database>
<database url="{{DB_ACHIEVEMENTS}}">Achievements & Responsibilities</database>
<database url="{{DB_SKILLS}}">Skills</database>
## 🎯 Search
<database url="{{DB_TARGET_ROLES}}">Target Roles</database>
## 📚 Tracking
<database url="{{DB_APPLICATIONS}}">Application Tracker</database>
## 📈 Growth and LinkedIn
<database url="{{DB_LEARNING}}">Learning Log</database>
<database url="{{DB_RESEARCH}}">Research</database>
<page url="{{PAGE_CV_RULES}}">CV Rules (ATS + AI agents)</page>
<database url="{{DB_SOURCES}}">Finder Sources</database>
<database url="{{DB_FINDER_LOG}}">Finder Log</database>
<page url="{{PAGE_FINDER_RULES}}">Daily Finder Rules</page>
<page url="{{PAGE_LINKEDIN}}">LinkedIn — Texts</page>
```

If the person has no "History notes" yet, keep the heading with the single explanatory bullet above.

## Guide pages (children of the hub)

| Page | Icon | Content |
|---|---|---|
| CV Rules (ATS + AI agents) | 📏 | Template below |
| Daily Finder Rules | 🔎 | `setup/finder/finder-rules.md`, filled in |
| LinkedIn — Texts | 💼 | `setup/linkedin-guide.md`, generated from the verified inventory (onboarding step 11) |

### CV Rules (ATS + AI agents)

```markdown
<callout icon="ℹ️" color="gray_bg">
	The rules the AI follows for every CV. The full version, with sources, is in docs/research/cv-rules.md of the project folder.
</callout>
## Format
- One column. No tables, columns, images, icons or skill charts.
- Standard headings: Summary, Skills, Experience, Projects, Education, Certifications, Languages.
- Dates with the full month name, one format in the whole document ("October 2025 – Present"). Never abbreviated ("Oct"): some parsers don't read it.
- English CVs have no accents or ñ, not even in proper names ("San Jose").
- Real text in a standard font (nothing inside images). PDF and DOCX are delivered.
- Plain characters only: no decorative bullets or symbols.
- Contact details in the body, never in the document header or footer.
- Two pages at most.
## Content
- **Only achievements with Verified checked.** Old CVs may be inflated; what is not verified does not go in.
- **Never invent.** Only what is in the inventory (Experience, Achievements, Skills). What is missing is reported as a gap.
- Every requirement of the job post needs visible evidence: the skill inside a concrete achievement, not only in the skills list.
- Use the job post's terms when they describe something the person really did (no stuffing).
- Numbers whenever they exist (volume, time, %, money).
- The CV headline is the exact title of the vacancy; job titles in Experience are never changed.
- No hidden text, prompt injection or keyword stuffing.
## Process for each vacancy
1. Read the job post and its link: required and preferred requirements, knockout questions, seniority, language, work mode.
2. Check eligibility from {{COUNTRY}} and ghost-job signals (date, reposts, vagueness, talent pools).
3. Read the whole inventory and build the requirement → evidence → gap match, with fit %.
4. Before calling something a gap, ask, one question at a time, whether the person ever did it. What they confirm is added to the inventory for future CVs.
5. Build the CV, run the 9 tests, show it, save it and record it in the Application Tracker.
## Consistency
- Same jobs, dates and data in the CV, LinkedIn and any personal site.
```
