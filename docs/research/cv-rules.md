Part of CV Factory by Johel Gomez Rojas — Apache License 2.0.

# CV rules (ATS + AI agents)

The rules CV Factory follows when it builds each CV. Each one points to where it comes from in the [research](README.md).

CV Factory makes **English CVs only**. The engine itself also supports Spanish, but this project is set to English, so the rules below describe English CVs.

## Structure (hybrid format, based on Harvard's professional version)

Section order for someone with experience [04 §4.1–4.3]:

1. **Header** (in the body, never in the document's header area): name · the title of the role being applied for · city and country, phone with country code, email, LinkedIn and portfolio URLs written in full.
2. **PROFESSIONAL SUMMARY:** 3–5 lines. Title + years + field + 2–3 achievements with numbers + what the person brings. No "I" and no "objective".
3. **SKILLS:** grouped by type, using the posting's terms, with the level in text.
4. **PROFESSIONAL EXPERIENCE:** reverse-chronological.
5. **PROJECTS:** optional; can go before Experience if it is more relevant to the role.
6. **EDUCATION:** official degree name, full institution name, city, country, date. It goes first only for students or recent graduates.
7. **CERTIFICATIONS:** name, issuer, year and expiry.
8. **LANGUAGES:** a single level framework, printed as "Language (level)", with the level as a plain phrase without parentheses: "Spanish (Native)", "English (C1, advanced)". In the inventory, languages are Skills rows with Category "Language" (Level, and the CEFR level in Notes).

Never: photo, age, marital status, children, gender, religion, full home address or references. Photo, national ID and nationality only if the company asks. [04 §4.6]

## Format

- **One column**, with no tables, text boxes, headers or footers, images, icons, skill bars or backgrounds. [01 §1.1] [05 §5.2]
- **Dates on the same line as the job title**, after a bar: `Title, Company | October 2025 – Present`. Or on the next line. **Never right-aligned** (they come apart from the title when the text is extracted). [05 §5.2]
- **No accents and no ñ, in proper names too** ("San Jose, Costa Rica", "Bogota", the person's own name). Reasons: a US recruiter searches without accents, not every system treats "José" the same as "Jose", and badly configured systems can turn "é" into "Ã©". The engine strips them itself and test 9 confirms none is left. The name should be written the same way (without accents) on LinkedIn and in each application form.
- **Proper names are never translated.** Institutions (schools, colleges, universities) go only with their original official name, with no translation in parentheses: "Bachelor's Degree in Business Administration, Universidad de Costa Rica". Company names are never translated either. Reasons: proper names are not translated, the degree text already tells the reader what the entry is, and adding the English translation made OpenResume (test 5) extract nothing when the line had both a degree keyword and a school keyword.
- **Dates with the full month name**, always the same way: "January 2021 – March 2023". Never abbreviated ("Jan"), never numbers only. Jobs and projects always have month and year (`YYYY-MM` in `cv.json`; if the month is missing, ask the person); education and certifications may show the year alone (`YYYY`). Reason: in the engine's tests, the OpenResume parser did not recognize "Jan 2021" as a date but did recognize the full name. [04 §4.5] [05 §5.6]
- **A standard, embedded font:** Calibri, Arial or Aptos (or their free equivalents Carlito, Liberation Sans, Noto Sans). Body 10.5–11 pt, name 14–16 pt bold, section headings 11–12 pt bold and uppercase. [04 §4.5]
- **Margins of 0.6–1 inch**, all equal, never under 0.5. Left-aligned, not justified. Black text. [04 §4.5]
- **Bold for title and company**; italics sparingly; never underline. [04 §4.5]
- **`•` bullets** in the same font as the text (never Word's default bullet). [05 §5.3]
- **No ligatures, no hyphenation, no letter spacing.** [05 §5.1]
- **Allowed characters:** letters, numbers, normal punctuation, en dash (–), bullet (•) and quotes. **Forbidden:** icons, emojis, decorative symbols (★ ✓ ▪), invisible spaces and soft hyphens. [05 §5.3]
- **Full job titles**, never abbreviated ("Senior", not "Sr."). [04 §4.5]
- **Length:** 1 page with less than about 5–7 years of experience; 2 at most after that. [04 §4.5]
- **Two files from the same source:** a PDF with real text (the default) and a DOCX. Under 1 MB. File name `First-Last-Resume.pdf`, with accents stripped and every part of the name kept (`Ana-Maria-Solis-Vargas-Resume.pdf`); title and author in the metadata. [05 §5.5]
- **Paper size by the employer's country:** US Letter for employers in the US, Canada, Mexico, Central America, Colombia, Venezuela and the Philippines; A4 elsewhere (the rest of South America, Spain, Europe). If unsure and the employer is in the US, Letter (`cv.json` → `paper`).
- **Test before sending:** copy the PDF's text and paste it into a plain text editor, or run the engine's automated tests. [05 §5.6]

## Bullets

- **Formula:** action + what and how + measurable result (Google's XYZ, or Project → Action → Result). If there is no number, a word that conveys value. [04 §4.4]
- Start with an action verb; past tense for previous roles, simple present for the current one. Never "Responsible for". [04 §4.4]
- 1–2 lines per bullet. Fragments, no pronouns. [04 §4.4]
- 4–6 bullets for recent, relevant roles; 2–3 for older ones. [04 §4.4]
- **One verifiable claim per bullet**, so an AI can quote it as evidence. [04 §4.7]

## Content

- **Only what is verified.** Anything the person has not confirmed stays out, even if it was on an old CV.
- **Never invent.** Anything missing is asked about or marked as a gap.
- **Be honest about technical skills.** Do not inflate a level to make it fit. If the person uses a tool with AI assistance, say so.
- **Every requirement in the job description gets explicit evidence:** the skill inside a concrete achievement, not only in the skills list. Screeners check requirement by requirement. [01 §1.2] [02 §2.2]
- **The posting's exact terms** when they describe something the person really did, without repeating them too much. [01 §1.2, §1.4]
- **Acronym and full name:** "Family and Medical Leave Act (FMLA)". [01 §1.4]
- **CV headline aligned with the role** being applied for, and true to what the person did. [01 §1.3]
- **Achievements with numbers** when they exist (good practice, though no study measures it). [01 §1.3]
- **Employment gaps filled with something real** (study, projects, freelance work). [01 §1.3]
- **Clear, direct wording:** AI models change their decision depending on how a CV is written. [02 §2.3]
- **The CV is written in the language of the job description** (in this project, English postings).
- **No hidden text, prompt injection or keyword stuffing.** [02 §2.4]
- **Education and Experience are never removed to make a test pass.** If a test fails because of how an entry is written, the agent stops and tells the person what failed instead of removing content.

## For each posting

1. Pull out of the job description: required and preferred qualifications, likely knockout questions, seniority, language, work arrangement and eligible countries.
2. **Check whether the person is eligible from their country** (many "remote" postings are US-only; healthcare has legal restrictions). [03 §3.1]
3. Look for signs of a ghost job (posting date, reposts, vagueness). [01 §1.6]
4. Build the requirement → evidence → gap matrix and compute the fit percentage.
5. **Before calling something a gap, ask the person** whether they have ever done that function or something similar. If so, add it to the profile.
6. If the fit is low or there is a certain knockout, recommend not applying.
7. Generate the CV, the answers to the knockout questions (including work authorization) and a short, specific cover letter only if one is requested. [01 §1.5] [03 §3.1]
8. Look for a contact or referral at the company. [01 §1.6]
9. Recommend applying on the company's own site, within the first week after posting. [03 §3.3]
10. Log the posting in the tracker.

## Consistency

- Same titles, dates and details on the CV, LinkedIn and any personal website (fraud filters cross-check data). [02 §2.5]

## Scope of the OpenResume test (test 5)

OpenResume is a parser built for US resumes. The engine uses it with two adjustments, documented so nobody thinks a failure is being hidden:

- **Accents:** OpenResume drops names with accents. English CVs have none (see the rule above). For non-English CVs, test 5 checks only name and contact; jobs and education are covered by tests 4 and 6.
- **Education without an English keyword:** if an education entry of an English CV has no school or degree word that OpenResume recognizes (e.g. "SENA"), test 5 only notes it and tests 4 and 6 verify the education; an entry with such a keyword must be extracted. It never forces dropping Education.
- **Phones outside the US:** OpenResume only recognizes 10-digit US numbers. A number with another country code is reported as a note, not a failure, and the phone is checked by tests 4 (it is in the first 5 lines) and 6 (the AI copies it exactly).

## Findings while building the engine (October 2026)

- **The font has to actually load.** A template bug made Chromium silently use Liberation Serif instead of Carlito. Now the engine stops if Carlito does not load, and test 1 fails if the PDF uses another font.
- **`text-rendering: geometricPrecision` is required.** Chromium does not write spaces into the PDF: readers guess them from the distance between words. With Carlito and without that line, pdfium glued words together after an "s" ("claimsspecialist", "systemsin") and test 2 dropped to 90.8 %. With the line, all 4 readers read 100 %.
- **Education with two or more degrees and no bullets:** OpenResume merges them into one (it separates entries by space between lines, or by a bold line after a non-bold one). Fix: a true detail line under the first degree (for example, its courses). OpenResume also recognizes schools only by English words ("Institute", "University", "School") and penalizes numbers on the line, so the high school year can be left out. Adding the English translation of the institution in parentheses was tried and dropped: when the line had both a degree keyword and a school keyword, OpenResume extracted nothing. The institution goes only with its original official name; an entry with no English school or degree keyword (e.g. "SENA") is only noted by test 5, and an entry with a keyword must be extracted.
- **Degrees in progress:** the line "degree, institution | In progress" wrapped onto two lines and OpenResume counted one job too many. Fix: the entry has no date (no `end` in `cv.json`) and its courses bullet starts with "In progress.". (Acronyms in parentheses, such as "Universidad Nacional (UNA)", also kept OpenResume from recognizing the institution: write the official name without them.)
- **A date range never breaks across two lines:** if the title line is long, the whole range moves down (the template marks it as unbreakable).
- **A hyphenated word never breaks at the end of a line:** "return-to-work" was split into "return-" / "to-work"; pdfium read it as U+FFFE (test 9 failed) and pdf.js as a broken word (test 3 failed). Now the template wraps every hyphenated word in a `<span class="nobr">` with `white-space: nowrap` (the `nobr` filter in `engine/scripts/render_pdf.py`).
- **A job never starts at the top of a new page:** OpenResume glues it to the previous job. The template moves the page break inside the previous job's bullets.
- **What goes into each CV (design choice):** older or less relevant jobs stay (ATS compute years of experience from the dates) but with a single bullet; the same employer in two separate periods gets two entries; projects go in only when the posting asks for something they demonstrate; 2 pages at most, with the strongest material on the first.

## Reading the data and asking (required for every CV)

- **A complete reading, every time:** every row of the experience, achievements and skills databases (the unverified ones too), every page opened, plus the other hub pages. The engine checks that the row count matches the source and that no page was skipped; otherwise it does not generate the CV.
- **Ask before assuming:** if the posting asks for something that is not in the data but the person might have, if something is ambiguous or if something is unverified, ask the person, one question at a time. Whatever they confirm is added to the source before it is used. Anything unconfirmed stays out.
