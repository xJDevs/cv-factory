Part of CV Factory by Johel Gomez Rojas — Apache License 2.0.

# 1. How ATS and recruiters process CVs

Research from October 2026. Every finding says where it comes from and how much to trust it:

- **Primary:** official vendor documentation, an academic study or a large first-party dataset.
- **Vendor:** a survey or data from a company that sells hiring or CV tools (it has a commercial interest).
- **Anecdotal:** a one-person test or a figure with no clear source.

Most "X times more interviews" figures are correlations, not causes.

---

## 1.1 Reading the file (parsing)

**What breaks parsing, according to the vendors themselves.** Greenhouse lists these causes of failure: files over 2.5 MB, CVs uploaded as images, tables, headers and footers, graphics, photos and columns. Workday says results "may vary based on formatting and word order" and recommends CVs without images. Workday also **does not fill** the skills or languages fields from the CV: candidates have to type them into the form.
Sources: [Greenhouse Support](https://support.greenhouse.io/hc/en-us/articles/200989175-Unsuccessful-resume-parse) · [Workday Admin Guide](https://doc.workday.com/admin-guide/en-us/human-capital-management/recruiting/candidates/set-up-prospects-and-candidates/hdc1552497830785.html) — Primary.

**The real risk is a scanned or image-only PDF.** Textkernel, the parser behind many ATS, only reads scanned PDFs with an optional OCR add-on. Without it, the CV can arrive empty.
Source: [Textkernel docs](https://developer.textkernel.com/TKPlatform/master/file-formats/) — Primary.

**Columns are not the problem in themselves; text order is.** Textkernel estimates that at least 15 % of CVs use columns and that reading them well is "surprisingly difficult". After an improvement, correctly parsed column CVs rose from 62 % to 90 %. A test of 36 layouts in 3 parsers found that some two-column designs parsed perfectly while others broke the experience section apart. The takeaway: what fails is the order in which the PDF stores its text.
Sources: [Textkernel blog](https://textkernel.com/learn-support/blog/improving-extraction-from-column-resumes) — Vendor · [Resumap, DEV](https://dev.to/resumap/we-ran-the-same-resume-through-4-real-ats-parsers-in-36-layouts-same-text-different-parses-3mfc) — Anecdotal.
→ **What to do:** one column is safest. To check a PDF, copy all its text and paste it into a plain text editor. If it comes out in the right order, an ATS will read it well too.

**PDF or Word: sources disagree.** Jobscan (2025) now recommends PDF because, according to its tests (no published data), it parses better. Greenhouse and Textkernel treat a PDF with real text and a DOCX the same. Everyone agrees that the image-only PDF is the one that fails.
Source: [Jobscan](https://www.jobscan.co/blog/resume-pdf-vs-word/) — Vendor.
→ **What to do:** a PDF with real text by default; a DOCX if the posting asks for one.

**Fake or test data gets rejected.** The Sovren parser (now Textkernel) rejects CVs with test or fake data, and Greenhouse lists "fake or poorly disguised data" as a cause of failure.
Source: [Sage People](https://help-people.sage.com/Content/SP_Talent_Acq/Use/SP_TalentAcq_Use_ResumeParsing.htm) — Primary.

**Length: one or two pages perform about the same; three or more do worse.** Huntr (real data, 2025): 1 page 3.06 % interview rate, 2 pages 3.24 %, 3 pages 2.6 %, 4+ pages 2.12 %. A ResumeGo experiment (2018, simulated) found recruiters chose two-page CVs 2.3 times more often, especially for mid-level and management roles.
Sources: [Huntr 2025](https://huntr.co/research/2025-annual-job-search-trends-report) · [ResumeGo](https://www.resumego.net/research/one-or-two-page-resumes/) — Vendor.
→ **What to do:** the "one page only" rule has no support. One page for little experience; two if there is relevant material.

**File name and typeface:** no evidence was found that either affects parsing or ranking.

## 1.2 How candidates are ranked and filtered

**Myth: "75 % of CVs are rejected by the ATS before a person sees them."** The figure comes from Preptel, a company that sold CV services, never published its method and closed in 2013.
Sources: [HiringThing](https://blog.hiringthing.com/applicant-tracking-system-myths) · [Lenz fact-check](https://lenz.io/c/ats-applicant-tracking-system-75-percent-rejection-rate-bc6fd7d4) — debunked.

**But real filters exist, set up by each company.** In interviews with 25 recruiters, 23 said their ATS does not reject for formatting. At the same time, a survey of 948 leaders says 50 % let AI reject at the CV stage. And the "Hidden Workers" study (Harvard and Accenture, 2021) found that more than 90 % of employers filter or rank with their system, and 88 % admit it screens out qualified candidates who are not an exact match.
Sources: [Enhancv](https://enhancv.com/blog/does-ats-reject-resumes/) — Vendor, small sample · [Resume Builder](https://resumebuilder.com/7-in-10-companies-will-use-ai-in-the-hiring-process-in-2025-despite-most-saying-its-biased/) — Vendor · [HR Dive on Hidden Workers](https://www.hrdive.com/news/report-applicant-tracking-systems-may-exclude-whole-segments-of-candidates/606614/) — Primary.
→ **The right reading:** software almost never rejects you for formatting. What decides who reaches a person are the rules and rankings each company configures.

**Knockout questions are the main documented automatic rejection.** Oracle: an answer with a negative score on a disqualifying question "automatically disqualifies" (its example: "Are you authorized to work in the United States?"). Greenhouse: auto-reject uses custom questions (example: "Requires visa"). Ashby: rules on form answers, such as location; the rejection email can be delayed by several days, so a slow rejection may still be automatic.
Sources: [Oracle](https://docs.oracle.com/en/cloud/saas/talent-management/faimh/create-a-disqualification-question.html) · [Greenhouse](https://support.greenhouse.io/hc/en-us/articles/203105595-Application-Rules-Overview) · [Ashby](https://docs.ashbyhq.com/auto-reject-applications) — Primary.
→ **What to do:** answers about work authorization, location, licenses and years of experience matter more than CV format. Prepare them for each posting.

**Workday HiredScore grades candidates A to D against the job description.** A: meets all basic and most preferred requirements. B: meets all basic ones. C: meets most basic ones. D: does not meet most of them. If the CV cannot be read, it **gets no grade** and probably sinks to the bottom of the list.
Source: [Workday HiredScore docs](https://doc.workday.com/hiredscore/en-us/workday-hiredscore/recruiter-productivity-/reference--candidate-grades.html) — Primary.

**Since August 2026, HiredScore can use a language model to check each requirement separately** (companies choose to turn it on). Meeting every basic requirement gives an A or B; missing one gives a C or D. It includes a "Fit & Gap" view.
Source: [HiredScore release notes, 5 Aug 2026](https://doc.workday.com/hiredscore/en-us/workday-hiredscore/hiredscore-release-notes/2026/august/wednesday--5th-august.html) — Primary (verified).
→ **What to do:** every requirement in the job description has to appear in the CV explicitly, with evidence.

**Greenhouse Talent Matching never rejects or advances anyone on its own, and more keywords do not raise the score.** It labels each candidate Strong, Good, Partial, Limited or "needs manual review" against weighted criteria the team defines.
Source: [Greenhouse Support](https://support.greenhouse.io/hc/en-us/articles/41131886674075) — Primary. It is the clearest statement from any vendor against keyword stuffing.

**Ashby checks criterion by criterion** (meets / does not meet / unsure, with its reasoning) and leaves the decision to people. If the candidate asks not to be evaluated by AI, the evaluation is skipped.
Source: [Ashby docs](https://docs.ashbyhq.com/ai-assisted-application-review) — Primary.

**Lever, iCIMS and SAP SuccessFactors** describe matching by skills and meaning, with no public technical detail.
Sources: [Lever](https://www.lever.co/levers-ai-innovations-are-here/) · [iCIMS](https://icims.com/talent-cloud-recruiting/platform/ai-recruiting-search-automation) · [SAP](https://www.sap.com/uk/products/hcm/successfactors-recruiting-applicant-screening.html) — Vendor.

**Skills ontologies merge synonyms.** Workday reduced one million user-written skills to 55,000 verified ones and found up to 20 synonyms for common skills.
Source: [Workday Newsroom](https://en-gb.newsroom.workday.com/Workday-Delivers-Machine-Learning-Powered-Skills-Cloud-to-Unlock-Untapped-Workforce-Potential) — Primary.

**But a recruiter's manual search is still literal in some systems.** Greenhouse search uses AND / OR / NOT and exact phrases, with no automatic synonyms.
Source: [Greenhouse](https://support.greenhouse.io/hc/en-us/articles/202360199-Search-candidates-using-Boolean-queries) — Primary.
→ **What to do:** AI understands synonyms, but a recruiter searching by hand does not. Use the job description's exact terms when they describe something the person really did.

**Who uses what.** 97.4 % of the Fortune 500 have an ATS; Workday holds about 40 %, SuccessFactors 12 %. Greenhouse holds 19 % in a broader sample of 13,000 companies.
Source: [Jobscan, Aug 2026](https://www.jobscan.co/blog/Fortune-500-use-applicant-tracking-systems/) — Vendor.

## 1.3 What recruiters look at

**The famous "6 seconds" only measures the first glance.** Ladders (eye tracking, 30 recruiters): 6 seconds on average, with 80 % of that time on name, current and previous title and company, dates and education. The 2018 update found 7.4 seconds, with more attention on job titles than on anything else. Simple layouts with bold titles and bulleted achievements won; columns and clutter lost. Other studies measure anywhere from an 11-second first glance to a 94-second full review.
Sources: [HR Dive on Ladders 2018](https://www.hrdive.com/news/recruiters-spend-74-seconds-looking-at-your-resume/541582/) · [InterviewPal](https://www.interviewpal.com/blog/how-long-recruiters-actually-spend-reading-your-resume-data-study) — Vendor.
→ **What to do:** make the job title, company and dates readable at a glance.

**A title that matches the posting is associated with 10.6 times more interviews.** Also: a university degree 6.1 times, a cover letter 3.4 times, an optimized LinkedIn profile 2.2 times (2.5 million applications). In the survey of 384 recruiters, 76 % start by filtering on skills, 43 % filter by location and 73 % check LinkedIn always or almost always.
Source: [Jobscan, Feb 2025](https://www.jobscan.co/blog/interview-rates-study) — Vendor, correlation (people whose title matches tend to be more qualified).

**Employment gaps do count in experiments.** With 12,054 fictional CVs, callbacks fell from about 7 % after 1 month out of work to about 4 % after 8 months. Yet 79 % of managers say they would hire someone with a gap.
Sources: [J-PAL on Kroft et al.](https://www.povertyactionlab.org/evaluation/dependence-duration-and-labor-market-conditions-evidence-united-states) — Primary · [The Hustle on LinkedIn](https://thehustle.co/03042022-job-gaps) — Vendor.
→ **What to do:** if there is a gap, fill it with something real (study, projects, freelance work) instead of leaving it empty.

**Numbers in achievements:** no controlled study was found that isolates their effect. It is good practice, not evidence.

## 1.4 Keywords

**Write both the acronym and the full term.** In Taleo, searching "project manager" does not find "project management", and "Certified Public Accountant" does not find "CPA". Example: "Master of Business Administration (MBA)".
Source: [Jobscan on Taleo, Apr 2026](https://www.jobscan.co/blog/taleo-popular-ats-ranks-job-applications/) — Anecdotal, but consistent with Greenhouse's literal search.

**Tailoring the CV is associated with more interviews:** 5.71 % tailored versus 3.09 % untailored (1.85 times). The gap narrows when comparing the same person, so part of the effect is about who tailors.
Source: [Huntr Q2 2026](https://huntr.co/research/job-search-trends-q2-2026) — Vendor (verified).

**Better writing means more hires, in a real experiment.** Almost 500,000 people on a work platform: those who received writing help were hired 8 % more often, with no drop in employer satisfaction.
Source: [NBER 30886](https://www.nber.org/papers/w30886) — Primary (randomized experiment).

## 1.5 Cover letters

**Before 2023 they helped.** An experiment with 7,287 applications: a tailored letter got 53 % more callbacks than no letter. Surveys: 83–87 % of managers say they read them.
Sources: [ResumeGo](https://www.resumego.net/research/cover-letters/) · [Resume Genius](https://resumegenius.com/blog/cover-letter-help/cover-letter-statistics) — Vendor.

**With AI, the generic letter lost its value.** On Freelancer.com, once a one-click AI writer was added, personalized proposals stopped predicting who got hired or did the job well. Only about 20 % of managers would reject an AI-written letter, but they identify AI CVs only a third of the time.
Sources: [Tuck/Dartmouth, Jan 2026](https://tuck.dartmouth.edu/news/articles/what-happens-to-hiring-when-ai-writes-job-applications) — Primary · [TopResume](https://topresume.com/career-advice/ai-in-hiring-survey) — Vendor.
→ **What to do:** a short, specific letter with details only that person could give. Nothing generic.

## 1.6 Volume and response rates

**Applications per role have tripled since 2021**, to more than 300 per role (Ashby, 100 million applications). Greenhouse: +134 % since ChatGPT launched. LinkedIn: about 11,000 applications per minute.
Sources: [HR Dive on Ashby, May 2026](https://www.hrdive.com/news/recruiters-see-job-applications-triple-to-more-than-300-per-role/820096/) · [Greenhouse](https://www.greenhouse.com/newsroom/greenhouse-unveils-new-ai-driven-products-at-unleash-to-streamline-hiring-in-saturated-job-market) — Primary / Vendor.

**The funnel:** 8 % of applicants pass the first screen and 0.5 % get an offer (about 1 hire per 200 applications). Recruiters handle 93 % more applications than in 2021, with 14 % fewer staff.
Source: [Gem 2026 benchmarks](https://vercel-legacy.gem.com/blog/key-takeaways-from-the-2026-recruiting-benchmarks-report) — Primary (165 million applications).

**Referrals win by a wide margin.** From application to interview: 40 % with a referral versus 3 % without. But only about 1 % of applications are referred. Gem: referrals convert 11 times better; candidates sourced by the recruiter, about 8 times.
Source: [Ashby Talent Trends](https://www.ashbyhq.com/talent-trends-report/reports/referrals) — Primary (verified).

**By channel (Huntr):** the company's own site gives a 6.42 % interview rate versus 3.82 % on job boards. Across platforms: Google Jobs 11.3 %, Wellfound 6 %, Glassdoor 5.5 %, Indeed 4.5 %, LinkedIn 3.1 %. Only 27.5 % got any interview through LinkedIn Easy Apply.
Sources: [Huntr Q2 2026](https://huntr.co/research/job-search-trends-q2-2026) · [Huntr 2025](https://huntr.co/research/2025-annual-job-search-trends-report) — Vendor.

**How long it takes:** a median of 82 days to the first offer and 23 days to the first interview. Of those who got an offer, 61 % needed 50 applications or fewer; 17 % needed more than 100.
Source: [Huntr Q2 2026](https://huntr.co/research/job-search-trends-q2-2026) — Vendor (verified).

## Contradictions and myths

1. **"75 % rejected by the ATS":** no source. The reality: rules and rankings each company configures.
2. **PDF or Word:** both work if they contain real text; the image-only PDF is the one that fails.
3. **One or two pages:** about the same; three or more do worse.
4. **"6 seconds":** that is the first glance, not the full review.
5. **Employment gaps:** managers say they do not matter; experiments say they do.
6. **Cover letters:** they helped before 2023; today they only help when they are specific.
