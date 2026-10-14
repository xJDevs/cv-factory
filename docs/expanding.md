<!-- Copyright 2026 Johel Gomez Rojas. Part of CV Factory. Licensed under the Apache License, Version 2.0 (see LICENSE and NOTICE). Do not remove this notice. -->

# Expanding CV Factory safely

CV Factory is meant to grow with you. The rule is simple: **expand, don't modify.** Add what you need around the engine, and leave the engine as it is unless you really know what you are doing.

## Safe to add or change (no technical knowledge needed)

| What | Where | How |
|---|---|---|
| Companies or job boards for the finder | Notion *Finder Sources* (or the Finder Sources sheet) | Add a row with the URL, Active checked and the reason. Start Notes with "Has date: yes" if the site shows posting dates. Or ask the AI to research and add them. |
| Finder rules: minimum fit, alert, volume, salary, windows | Notion *Daily Finder Rules* (Excel: `my-data/finder-rules.md`) | Edit the page, or ask the AI. The finder reads it on every run. |
| Finder times | The scheduled task (Notion only) | Ask the AI to change it. |
| Target roles | Notion *Target Roles* (or the Target Roles sheet) | Add rows, or change Priority (Discarded = the finder ignores it). |
| Your history, achievements and skills | The inventory | Ask the AI to add things. It verifies them with you. |
| Extra Notion views, pages or databases | Your CV Factory page | Anything you like. Do not rename the existing databases or their columns, and do not add filters to a database's **Default view** (the AI reads through it). Make a new view to filter. |
| Notes and documents of your own | Anywhere outside `engine/` | Free. |

## Possible, with care (some technical knowledge)

- **New instructions for the agent:** add them at the end of `AGENTS.md` under a heading such as "My additions". Keep the "Never" list as it is.
- **New sources in the starter catalog** (`setup/finder/sources-catalog.json`): check that the site can be read automatically and that its robots.txt allows it.

## Not recommended (core files)

Everything in **`engine/`**: the template (`cv.html.j2`, `cv.css`), the scripts, the 9 tests and the fonts. They were tuned through experiments so that CVs read correctly in applicant tracking systems, parsers and AI screeners. A small change, like a new font, a two-column layout, an icon or a table, can make CVs fail the tests or, worse, read badly in real systems.

`engine/MANIFEST.sha256` records the original release. Every time the setup (`engine/setup.py`) runs it compares the files and **warns** (it does not block) if any core file was changed, added or removed. If your CVs start failing after a change, restore the original files from the release you downloaded.

If you do change the engine: Apache 2.0 requires that you mark the files you changed, and you must keep the author notices and the `NOTICE` file. Run the example check afterwards on a copy (as in `setup/onboarding.md`, step 2: copy `engine/example/output/` to `my-data/reads/example-check/` and run `cv.py test` there) and make sure it still says `APPROVED`. Never write into `engine/example/output/`.
