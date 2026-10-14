<!-- Copyright 2026 Johel Gomez Rojas. Part of CV Factory. Licensed under the Apache License, Version 2.0 (see LICENSE and NOTICE at the project root). Do not remove this notice. -->

# Daily finder: the scheduled task

The finder is a scheduled AI task that runs in the cloud twice a day, even with the computer off. It reads and writes only in the person's Notion. The rules live in the Notion page **Daily Finder Rules** (from `finder-rules.md`); the task's own prompt (below) only says where things are and the limits.

**Requires Notion.** With the Excel workbook there is no daily finder: the cloud task cannot write to a file on the computer. Excel users ask for vacancies in a conversation ("look for vacancies for me") and the agent follows the local copy of the rules, `my-data/finder-rules.md`, by hand (see `AGENTS.md`, "Daily finder").

## Schedule

- **Recommended:** a full run early in the morning and a light recheck at midday, in the person's time zone. The defaults come from the author's setup in Costa Rica (UTC−6): **6:50 a.m.** (results are waiting before the day starts; it catches everything posted the day before and overnight) and **12:50 p.m.** (by then the US morning, when many remote roles are posted, is over, so it catches what was posted that same morning).
- **Convert to the person's time zone** by the same logic: the morning run before their working day starts, the midday run after the US morning (about 2:50 p.m. US Eastern in summer). Explain the reason and let them choose other times; the minimum interval between runs is one hour.
- Write the cron with the time zone prefix, e.g. `CRON_TZ=America/Bogota 50 7,13 * * *`.

## Volume and cost (say this clearly at onboarding)

- The person chooses **10 or 20 vacancies per run** (`MAX_PER_RUN`). More vacancies, more sources and two runs a day mean longer sessions and **more use of their subscription or tokens**. That cost is the person's responsibility; the author of CV Factory is not responsible for any usage or charges.
- **Model:** use the most capable model available (today Claude Opus 5.5 or its equivalent in another AI). Smaller models miss eligibility details and inflate the fit.

## How to create it

**Claude (Claude Code or the Claude app):** create a cloud routine (Claude Code: the `/schedule` command or the RemoteTrigger tool; Claude app: a scheduled task). Settings:
- Name: `Daily job finder`.
- Schedule: the cron above, with the person's time zone.
- Model: the most capable one (e.g. `claude-opus-5-5`).
- Connector: **Notion** (the same account as the workspace). No repository, no local folders.
- Notifications: push on (the final message is the phone alert).
- Prompt: the block below, filled in.

**Other agents (Codex, Gemini, etc.):** use that tool's scheduled or background tasks if it has them, with a Notion connection and web access, and the same prompt. If it has none, the person asks for a search in a conversation.

After creating it, run it once by hand and check the Finder Log row and the vacancies it added.

## Prompt (fill in and paste)

```text
You are the daily job finder of {{FULL_NAME}} (lives in {{CITY}}, {{COUNTRY}}). Everything you need is in their Notion (Notion connector). Do not use their computer or any local folder.

1. Load the Notion tools (fetch, query-data-sources, create-pages, search) and WebFetch and WebSearch.
2. Read the page "Daily Finder Rules" ({{PAGE_FINDER_RULES}}) and follow it to the letter. If anything in this message conflicts with that page, the page wins, except for the limits below, which are never broken.
3. There are two runs a day. Check the current time in {{TIMEZONE}} (for example with bash: TZ={{TIMEZONE}} date). Before {{MIDPOINT_TIME}} it is the morning run; after, it is the lighter midday run. Follow what the rules page says for each one (time window, sources, log row name and final message).
4. Read the databases in VIEW mode only (query-data-sources with "mode": "view" on each Default view, page_size 100, following next_cursor until has_more is false). Never use SQL or rows mode: they have a usage quota and the run fails when it runs out.
   - Hub CV Factory (search preferences): {{HUB_URL}}
   - Target Roles: {{VIEW_TARGET_ROLES}}
   - Finder Sources: {{VIEW_SOURCES}} (only Active ones)
   - Experience & Education: {{VIEW_EXPERIENCE}}
   - Achievements & Responsibilities: {{VIEW_ACHIEVEMENTS}} (as evidence only Verified ones)
   - Skills: {{VIEW_SKILLS}}
   - Application Tracker (to avoid duplicates and to write): {{VIEW_APPLICATIONS}}
5. Read the sources with WebFetch (the URLs of the table; if they contain {keyword}, one query per keyword) and WebSearch (the queries; not needed in the midday run). Use today's date and time in {{TIMEZONE}} for the window the rules give.
6. Write the vacancies that pass (at most {{MAX_PER_RUN}} per run, fit {{MIN_FIT_PERCENT}} % or more) in Application Tracker (data source {{DS_APPLICATIONS}}) with the columns the rules give. Fit % is a number between 0 and 1. Date posted as "date:Date posted:start". Target role as a list with the URL of the role's page. Found by = "Daily finder".
7. If you find new companies that fit and whose careers site can be read for free, add them to Finder Sources (data source {{DS_SOURCES}}) with Active checked, as the rules say.
8. Write one row in Finder Log (data source {{DS_FINDER_LOG}}), even if you added no vacancy.
9. End with the final message the rules ask for (if one has {{ALERT_FIT_PERCENT}} % or more, on the first line).

Limits that are never broken: never apply to anything, never create accounts, never write to anyone, free sources only, do not try to read pages that block automated reading by other means, never invent experience, and in Notion only create new rows in Application Tracker, Finder Log and Finder Sources (do not edit or delete anything else).
```

`{{MIDPOINT_TIME}}` = a time between the two runs (e.g. 10:00 if the runs are at 6:50 and 12:50).
