<!-- Copyright 2026 Johel Gomez Rojas. Part of CV Factory. Licensed under the Apache License, Version 2.0 (see LICENSE and NOTICE). Do not remove this notice. -->

# AGENTS.md — instructions for any AI agent

> For Codex, Gemini, Cursor, Copilot or any other assistant working in this folder.
> **The source of truth is `CLAUDE.md`.** Read it completely and follow it. This file only explains how to translate the Claude-specific parts. If anything here conflicts with `CLAUDE.md`, `CLAUDE.md` wins, and its "Never" list is never broken.

## Before anything

1. Read `CLAUDE.md`, then `setup/onboarding.md` if `my-data/profile.json` is missing or the onboarding is not complete.
2. Read `engine/README.md` and `docs/research/cv-rules.md` before your first CV.
3. Run the setup: `python3 engine/setup.py` (macOS, Linux) or `py engine\setup.py` (Windows); it must end with `READY`. Then run the engine with `<PY>` as `CLAUDE.md` ("Running the engine") says: `engine/.venv/bin/python` or `engine\.venv\Scripts\python.exe`.

## Translating the Claude-specific parts

| `CLAUDE.md` says | If you are another agent |
|---|---|
| Notion MCP tools (`notion-fetch`, `notion-query-data-sources` in view mode, `notion-create-database`…) | Connect the official Notion MCP server (`https://mcp.notion.com/mcp`) in your tool's MCP settings. Same rule: read databases through their views, never SQL. Without Notion access, use the Excel branch. |
| `WebFetch` / `WebSearch` | Your tools to read web pages and search. Respect robots.txt. Never read LinkedIn, Indeed, Computrabajo or Remotive by any means: ask the person to paste the text. |
| 3 subagents to read the inventory | You can read the three databases yourself. Mandatory: every row, every page opened, `rows_in_source` equal to what the view returned. Then `build_snapshot.py`. |
| Test 6: two subagents with no context | Two new model calls **with no history**, each given only the block "Prompt to send (copy only this block)" of `engine/scripts/tests/t6_instructions.md`, plus its input file path and output JSON path (one with the PDF, one with `plain-text.txt`, both in the vacancy's `out/` folder). The grading section is for you, not for them. If you cannot do that, test 6 fails and the CV is not delivered. |
| Writing to the Excel workbook | Always `<PY> engine/scripts/workbook.py upsert` (see `CLAUDE.md`); never edit the `.xlsx` with other tools. |
| Show the CV (send the file) | Tell the person the path of the PDF in `CVs/Company - Role/`. |
| Look at the PDF as images | Render pages to PNG (`pdftoppm -png`, from poppler; on Windows `pdftoppm.exe`, in PATH or in `CVF_POPPLER_BIN`) and check them if you can see images; otherwise say so. |
| Cloud routine for the daily finder | Use your tool's scheduled/background tasks if it has them (with Notion and web access) and the prompt in `setup/finder/finder-prompt.md`. If it has none, the person asks for searches in a conversation. |
| A "project" in the Claude app | Your tool's equivalent (a workspace or project with instructions "Read AGENTS.md" and this folder attached). One conversation per CV. |

## How to talk to the person

Plain words, short answers, one question at a time in the chat, explain before big changes and wait for an OK. Never commit, push or merge without explicit permission each time.
