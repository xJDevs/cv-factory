Part of CV Factory by Johel Gomez Rojas — Apache License 2.0.

# Research: how hiring works in 2026

This is the evidence base behind CV Factory. It was researched in October 2026 from more than 150 sources, plus our own experiments with five PDF readers. Sources include official ATS documentation (Workday, Greenhouse, Oracle, Ashby), academic studies, reports built on millions of applications (Ashby, Gem, Huntr) and official sources from Latin America.

| File | What it covers |
|---|---|
| [01-how-ats-work.md](01-how-ats-work.md) | How a CV is parsed, filtered and ranked; what recruiters look at; keywords; cover letters; volume and response rates |
| [02-ai-agents-and-regulation.md](02-ai-agents-and-regulation.md) | AI screening, how LinkedIn's agent searches, model bias, candidates' own AI use, fraud and the law |
| [03-remote-market-latin-america.md](03-remote-market-latin-america.md) | How foreign companies hire in Latin America, where to look, tactics, scams and contractor taxes |
| [04-cv-format.md](04-cv-format.md) | The Harvard format, chronological vs. hybrid, section order, how to write bullets, typography, Latin America vs. the US |
| [05-generating-pdf-and-docx.md](05-generating-pdf-and-docx.md) | The technical side: text layer, reading order, characters, which tools to use for PDF and DOCX, and how to test them (with our own experiments) |
| [cv-rules.md](cv-rules.md) | The rules the engine applies, drawn from everything above |
| [experiments/](experiments/) | The scripts and test files behind the findings in 05 |
| [portal-tests/](portal-tests/) | What happened when a fictional CV was uploaded to real application forms |

## The 14 key points

1. **Competition is fierce.** Applications per role have tripled since 2021 (over 300 per role), and only about 0.5 % of applicants get an offer. → [01 §1.6]
2. **"The ATS rejects 75 % of CVs" is a myth with no source.** Software almost never rejects you for formatting. What rejects people automatically are the **knockout questions** each company sets up (work authorization, location, licenses, years of experience). → [01 §1.2]
3. **CVs are checked requirement by requirement.** Workday HiredScore (with a language model since August 2026), Ashby and LinkedIn's agent look for evidence of each requirement and quote it. If it is not written down, it does not exist. → [01 §1.2] [02 §2.2]
4. **Format matters for parsing, not looks.** The real risks are image-only PDFs and text that comes out scrambled. One column is safest; a PDF with real text or a DOCX both work. Two pages are fine; three or more do worse. → [01 §1.1]
5. **Keyword stuffing does not help** (Greenhouse says so explicitly), but a recruiter's manual search is literal. Use the posting's exact terms when they describe something real, and write both the acronym and the full name. → [01 §1.2, §1.4]
6. **The job title carries a lot of weight**, both for recruiters (it is what they look at most) and in the data (10.6 times more interviews when it matches). → [01 §1.3]
7. **Tailoring the CV to each posting** is associated with about 1.85 times more interviews, and better writing increased hiring in a real experiment. → [01 §1.4]
8. **AI models are sensitive to how a CV is written.** Changing only the wording flipped 30 % to 41 % of their decisions in one study. Form matters more than it used to. → [02 §2.3]
9. **Hidden text does not work** and gets you discarded. **Auto-apply bots** perform poorly and platforms block them. → [02 §2.4]
10. **Referrals win by a wide margin:** 40 % reach an interview versus 3 % without one. Applying on the company's own site beats job boards, and applying in the first week helps. → [01 §1.6] [03 §3.3]
11. **LinkedIn is a second CV, read by an agent.** It searches by meaning, refreshes daily and quotes evidence from the profile. Keep it complete, verified and consistent with the CV. → [02 §2.2]
12. **Global remote work is possible from Latin America, but competition is higher** (remote roles get 42 % of applications while being 8 % of postings), and in US healthcare many roles legally exclude people outside the US. Local hybrid roles often give better odds. → [03]
13. **The base format is Harvard's professional version, as a hybrid:** summary and skills on top, reverse-chronological experience, then education. A functional CV (no clear history) confuses ATS. → [04]
14. **Right-aligned dates come apart from the job title** when text is extracted (confirmed with five readers). Put them on the same line, after a bar. And no icons, ligatures or Word's default bullet. → [05]

## How to read the confidence labels

- **Primary:** official documentation, an academic study or a large first-party dataset.
- **Vendor:** a survey or data from a company that sells hiring or CV tools.
- **Anecdotal:** a one-person test or a figure with no clear source.

Almost every "X times more" is a correlation: it shows two things go together, not that one causes the other.

## How to update it

When a new data point appears, add it to the topic file with its source, date and confidence label. If it changes a rule, update [cv-rules.md](cv-rules.md) too.
