<!-- Copyright 2026 Johel Gomez Rojas. Part of CV Factory. Licensed under the Apache License, Version 2.0 (see LICENSE and NOTICE). Do not remove this notice. -->

# User guide

CV Factory brings job hunting down to one thing for you: **review and apply.** The AI does the rest.

| The AI does | You do |
|---|---|
| Look for vacancies every day in free sources (with Notion) | Search LinkedIn and other sites that block robots (with one-click links) |
| Check you can take the job from your country and that it is real | Decide where to apply |
| Score your fit and list what is missing | Answer its questions honestly |
| Build a CV for each vacancy and test it | Review the CV |
| Keep the application tracker | Apply and fill in the form |

**It never** applies for you, creates accounts, writes to recruiters, invents experience, or reads sites that forbid robots.

## 1. Before you start

- **An AI agent.** Claude Code or the Claude desktop app is recommended. Other agents work too: they follow `AGENTS.md`. **Use the most capable model you have** (today Claude Opus 5.5 or its equivalent), both for CVs and for the daily finder. Smaller models make more mistakes.
- **A Mac, Linux or Windows 10/11 computer.** You do not type any commands: the AI runs them. The setup installs what it can and tells you what is missing, and the AI explains it. Usually:
  - **Mac:** Homebrew (https://brew.sh), then `brew install python poppler node` and `brew install --cask libreoffice`.
  - **Windows:** five programs, installed from PowerShell with winget: `winget install -e --id Python.Python.3.13`, `winget install -e --id OpenJS.NodeJS.LTS`, `winget install -e --id oschwartz10612.Poppler`, `winget install -e --id TheDocumentFoundation.LibreOffice` and `winget install -e --id Git.Git`. **Claude Code on Windows needs Git for Windows** (the last one). Close and reopen the agent afterwards.
  - **Linux:** the AI gives you one `sudo apt install ...` line.
  - It is tested on macOS; Windows and Linux are covered by automatic tests (the CI workflow).
- **Notion (recommended, free)** or Excel. See section 3.
- **Your history:** old CVs (ideally 5 or more), your LinkedIn profile as a PDF, a document with your experience, or just the will to tell it.
- **Costs:** your AI subscription or tokens are yours to manage. The more work you give the AI (more vacancies, more sources, two finder runs a day), the more it uses. Read [`DISCLAIMER.md`](../DISCLAIMER.md).

## 2. Install

1. Put the folder on your **Desktop** and name it **`cv-factory`**. On Windows, if OneDrive backs up your Desktop, the Desktop is `C:\Users\<your name>\OneDrive\Desktop`; that works too (the AI finds it), but OneDrive will copy the folder, including your private data, to your OneDrive account. If you prefer it not to, keep the folder outside OneDrive (for example `C:\Users\<your name>\cv-factory`).
2. **Create a project in your agent** (for example a Project in the Claude app):
   - Instructions: *"Read AGENTS.md in the linked folder and follow it."* (the same for every agent).
   - Link or attach the `cv-factory` folder.
3. Open a conversation in that project and say hello. The **onboarding** starts on its own (`setup/onboarding.md`). It asks one question at a time and remembers where it stopped, so you can do it in several sittings.

**One conversation per CV.** After the onboarding, start a new conversation inside the project for every vacancy. It keeps each CV clean.

## 3. Notion or Excel

The AI asks **"Do you use Notion?"** and strongly recommends it:

- It is **free** for personal use.
- **The daily finder runs in the cloud, even with your computer off**, and needs an online place to write the vacancies it finds. Notion is one; a file on your computer is not.
- The AI reads your inventory live for every CV and saves there what you confirm.
- You can filter and sort vacancies (by status, fit, calls vs back office) and see everything on your phone.

Without Notion, everything goes into one Excel workbook (`my-data/career-workbook.xlsx`, one sheet per table), and your contact details and preferences stay in `my-data/profile.json`. CVs work the same. The one difference: **no automatic daily finder**. You ask for vacancies in a conversation ("look for vacancies for me") and the AI follows your rules in `my-data/finder-rules.md`. The workbook has no Learning Log, Research or Finder Log (those are Notion only).

Your Notion gets a **CV Factory** page with: Experience & Education, Achievements & Responsibilities, Skills, Target Roles, Application Tracker, Learning Log, Research, Finder Sources, Finder Log, and three guides (CV Rules, Daily Finder Rules, LinkedIn — Texts).

## 4. Your inventory (the most important part)

The AI turns your history into rows: every job, every achievement, every skill. Then it checks each achievement with you: *"Is this exactly true?"* **Only what you confirm (Verified) can appear in a CV.** If an old CV inflated a number, keep the conservative one. If you have an official record of your dates, it is the best source.

Lying is not welcome, and it does not help either: the system is built on true information, and anything false you give it is your responsibility.

## 5. How vacancies are found

**Path A — Daily finder (Notion).** It runs twice a day. Recommended: a full run early in your morning and a recheck at midday; the AI suggests times for your time zone (the author uses 6:50 a.m. and 12:50 p.m. in Costa Rica), and you can choose other times. It:

- looks in remote job boards, boards for your region and country, company career sites and web searches (the list is in *Finder Sources*; you can add companies, and it adds new ones it finds);
- discards vacancies you cannot take from your country, ghost jobs, those that pay below your minimum, and those below **75 % fit**;
- leaves up to **10 or 20 per run** (you choose) in the Application Tracker as "To review";
- alerts your phone when one scores **85 % or more**.

**Path B — LinkedIn and other blocked sites (by hand).** LinkedIn forbids robots, and an account that is automated can be restricted. Use the quick-search links of your LinkedIn texts: the *LinkedIn — Texts* page in Notion, or `my-data/linkedin-texts.md` with Excel (last 24 hours, one keyword each). When something looks good, paste its **link and job description** to the AI.

From the job description on, both paths are the same.

## 6. Getting a CV

Open a new conversation in the project and paste the **link and the job description**. Or mark vacancies as **"Will apply"** in the tracker and say *"make the CVs for the ones I marked"*. The AI:

1. Checks you can take it from your country and that it is not a ghost job.
2. Reads your whole inventory.
3. Shows a requirement-by-requirement table with your fit % and gaps.
4. Asks, one question at a time, about things the vacancy wants that you might have done. What you confirm is saved for future CVs.
5. Builds the CV (PDF and Word) and runs the **9 tests**. It never hands you one that fails.
6. Shows it to you, saves it in `CVs/Company - Role/` and records it in the tracker as "CV ready".

Your job: **review, apply, and say "I applied"**. It records the date and a follow-up in 7 days.

This project makes **English CVs**.

## 7. Reading the Application Tracker

| Column | Meaning |
|---|---|
| Fit % | How well you match the requirements. Capped at 70 % if you lack experience in the role's main area. |
| Gaps vs job post | What the vacancy asks that is not in your inventory |
| Work type | Back office (almost no calls), Calls, Mixed or Unconfirmed |
| Eligible from my country | The sentence of the vacancy that proves you can take it |
| Source | Where it was found. "Finder (unverified)" = open the link and confirm it first |
| Status | To review → Will apply → CV ready → Applied → Interview → Offer / Rejected / Discarded |

## 8. When applying

- **Always check the form fields.** Many portals fill them from your CV, and some do it badly.
- Use exactly the same details as your CV (name, phone, LinkedIn, location).
- Answer knockout questions (years of experience, salary) consistently with the CV.

## 9. Expanding it

You can add finder sources, target roles, Notion views or pages, and documents. Changing the engine is not recommended. See [expanding.md](expanding.md).

## 10. Questions

**Why doesn't it search LinkedIn directly?** LinkedIn forbids it and can restrict your account. Search there by hand with the quick links and paste the job description.

**What does "unverified" mean?** The finder saw the vacancy in a web search but could not open it. Open the link and confirm before asking for a CV.

**Can I change the rules (minimum salary, minimum fit, times, volume)?** Yes: in Notion, on the *Daily Finder Rules* page (with Excel, in `my-data/finder-rules.md`), or ask the AI.

**What if a CV says something I didn't do?** It shouldn't happen: every sentence comes from a verified row. If it does, fix the row in your inventory and regenerate.

## 11. Privacy

Your data lives on your computer (`my-data/`, `CVs/`) and in your own Notion. The AI provider you use processes what you share with it under its own terms. Nothing is published or sent anywhere unless you do it.
