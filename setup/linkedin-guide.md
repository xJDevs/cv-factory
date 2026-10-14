<!-- Copyright 2026 Johel Gomez Rojas. Part of CV Factory. Licensed under the Apache License, Version 2.0 (see LICENSE and NOTICE at the project root). Do not remove this notice. -->

# LinkedIn — Texts: how to generate the page

The **LinkedIn — Texts** page (in Notion, or `my-data/linkedin-texts.md` without Notion) is the person's whole LinkedIn profile, ready to copy, in the order LinkedIn shows it. The person does every change by hand: **LinkedIn forbids automating a profile**, so the AI never logs in, never edits and never scrapes LinkedIn.

## Rules for the agent

- Everything comes from the inventory: only **Verified** achievements, the official job titles (English title), real dates. Same rules as a CV: nothing invented.
- Each actionable item is a **to-do** (`- [ ]`). Text to paste goes in a ` ```plain text ` code block right after its to-do (in Notion that gives it a copy button). Field labels in bold, separated by ` · `.
- Respect LinkedIn limits: headline 220 characters, About 2,600, 5 top skills, 5 skills per position, 5 "open to work" titles from LinkedIn's own list.
- Write the counts ("154 of 220 characters") so the person knows it fits.
- Ask before including anything sensitive (current employer if they are job hunting quietly, phone number in contact info).
- **Start from the person's current profile:** ask them to download it as a PDF (More → Save to PDF) and use it to mark each item as new, fix or remove. That PDF is also a good source for the inventory (onboarding step 3), but only after the person confirms each item.
- **Maintenance:** whenever something new is added to the inventory (achievement, project, course), prepare its LinkedIn text and add it to this page, in a "New" section at the top, unchecked.
- **Without Notion** (`my-data/linkedin-texts.md`): the template is the same, except that callouts are written as blockquotes (`> ℹ️ Texts ready to copy…`). Keep the to-dos (`- [ ]`) and the code blocks as they are.

## Quick searches (the most used part)

LinkedIn cannot be read by the daily finder. These links let the person check it by hand in one minute a day.

- Pattern: `https://www.linkedin.com/jobs/search/?keywords=%22<keyword>%22&location=<location>&f_TPR=r86400&f_WT=<work type>`
- `keywords`: one short keyword per link, as an exact phrase in quotes (`%22`), spaces as `%20`. Take them from **Target Roles** (Priority not Discarded): the Role and the most common Equivalent titles, 1–3 words as they appear in job titles ("claims specialist", "benefits analyst").
- `location`: URL-encoded LinkedIn location: the person's country for the first group, their region for the second (e.g. `Latin%20America`), or a city if they only want on-site/hybrid near home.
- `f_TPR=r86400`: posted in the last 24 hours (`r604800` = 7 days).
- `f_WT`: work type: `1` on-site, `2` remote, `3` hybrid; several separated by `%2C`. Country group: `2%2C3` (remote and hybrid) unless the person wants on-site too. Region group: `2` (remote only).
- Link text: `<Keyword in Title Case> · <Location>`.
- First group: all keywords (10–15). Second group: the top ~6.

## Page template

```markdown
<callout icon="ℹ️" color="gray_bg">
	Texts ready to copy into LinkedIn, in the order of the profile. Every grey block has a copy button. Check each step when done. Everything comes from the verified inventory. Version 1, {{MONTH_YEAR}}.
</callout>
## 0. Before you start
- [ ] **Download your current profile as a PDF:** on your profile, click **More** (or **Resources**) → **Save to PDF**. Give that PDF to the AI: it compares it with your inventory and marks below what to add, fix or remove.
- [ ] **Repeat it every few months** (or after big changes) so the AI can check that LinkedIn and your CVs still say the same thing.
## Focus
{{ONE_PARAGRAPH: which roles this profile targets and why}}
## 1. Intro
- [ ] **First name:** {{FIRST_NAME}} · **Last name:** {{LAST_NAMES}} (same spelling as the CV)
- [ ] **Headline** ({{N}} of 220 characters):
```plain text
{{AREA | MAIN ROLE | SECONDARY AREAS | DIFFERENTIATOR | LANGUAGES}}
```
- [ ] **Location:** {{CITY}}, {{COUNTRY}}
- [ ] **Industry:** {{LINKEDIN_INDUSTRY}}
- [ ] **Contact info:** {{WHAT_TO_KEEP_OR_REMOVE}}
## 2. About ({{N}} of 2,600 characters)
- [ ] Paste:
```plain text
{{Hook line. Years of experience and where. One "• Area (Employer): ..." paragraph per main role with verified numbers. "What I bring: ...". Side projects, if any. "Languages: ...". "Open to <work mode> roles in <areas>."}}
```
- [ ] **Top skills** (under About, 5 at most): {{SKILL_1}} · {{SKILL_2}} · {{SKILL_3}} · {{SKILL_4}} · {{SKILL_5}}
## 3. Experience
Newest first.
### 3.1 {{EMPLOYER}} ({{new / fix}})
- [ ] **Title:** {{ENGLISH_TITLE}} · **Location:** {{CITY}}, {{COUNTRY}} · **Dates:** {{START}} – {{END or "I currently work here"}}
```plain text
• {{verified bullet}}
• {{verified bullet}}
```
(Several titles at one employer: one to-do + code block per title, added with "Add position" inside the same company.)
### 3.N Skills for each position
In the Skills field of each position. Ignore LinkedIn's suggestions that are not here.
- [ ] **{{EMPLOYER — TITLE}}:** {{skill}} · {{skill}} · {{skill}} · {{skill}} · {{skill}}
## 4. Education
- [ ] **Add / fix:** {{INSTITUTION}} · **Degree:** {{DEGREE}} · **Field of study:** {{FIELD}} · **Dates:** {{START}} – {{END}} · **Description:**
```plain text
{{optional: coursework or focus}}
```
## 5. Licenses & certifications
- [ ] **Name:** {{NAME}} · **Issuer:** {{ISSUER}} · **Issued:** {{MONTH_YEAR}} · **Expires:** {{MONTH_YEAR}} · **Credential ID:** {{ID}}
## 6. Projects
- [ ] **{{PROJECT}}** · {{START}}
```plain text
{{what, for whom, measurable result, built with ...}}
```
- [ ] **Skills:** {{skill}} · {{skill}} · {{skill}} · {{skill}} · {{skill}}
## 7. Languages
- [ ] {{LANGUAGE}} · {{Native or bilingual | Full professional | Professional working | Limited working | Elementary}}
## 8. Skills
- [ ] **Remove:** {{SKILLS_TO_REMOVE}}
- [ ] **Add** (the first 5 are the top skills):
```plain text
{{one skill per line, about 25}}
```
## 9. Open to work (recruiters only)
- [ ] **Visibility:** "Recruiters only" (no green frame on the photo).
- [ ] **Job titles** (5 at most, only from LinkedIn's list; broad enough not to box you in): {{ROLE_1}} · {{ROLE_2}} · {{ROLE_3}} · {{ROLE_4}} · {{ROLE_5}}
- [ ] **Work mode:** {{WORK_MODES}}
- [ ] **Locations:** {{LOCATIONS}}
## 10. Quick searches on LinkedIn (last 24 hours)
Shortcuts to check LinkedIn by hand (the daily finder cannot read LinkedIn). Open them once a day. Each link searches one keyword and only vacancies posted in the last 24 hours (`f_TPR=r86400`). Look only at the results above the grey box "We found more results related to your search"; what is below does not match. On each vacancy you like, open "Show match details" and, if it is worth it, paste the link and the job description to the AI. To look further back, change the number in the URL: 604800 = 7 days.
### {{COUNTRY}} (remote or hybrid)
- [{{Keyword}} · {{COUNTRY}}](https://www.linkedin.com/jobs/search/?keywords=%22{{keyword}}%22&location={{COUNTRY_ENCODED}}&f_TPR=r86400&f_WT=2%2C3)
### {{REGION}} (remote)
- [{{Keyword}} · {{REGION}}](https://www.linkedin.com/jobs/search/?keywords=%22{{keyword}}%22&location={{REGION_ENCODED}}&f_TPR=r86400&f_WT=2)
## 11. For later
- **Featured:** when there are posts or a personal site.
- **Website** in contact info, when it exists.
- **Maintenance:** with every new item in the inventory, the AI prepares its LinkedIn text and adds it here.
```
