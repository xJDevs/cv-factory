Part of CV Factory by Johel Gomez Rojas — Apache License 2.0.

# 2. AI and agents in hiring, and the laws that regulate them

Research from October 2026. Same confidence labels as in [01](01-how-ats-work.md): Primary, Vendor, Anecdotal.

---

## 2.1 How much AI is used for screening

**Most companies already use it, and screening CVs is the most common use.** Resume Builder (948 leaders, Oct 2024): 51 % used AI in hiring; of those, 82 % to review CVs. Resume Genius (Jun 2026): 87 % use AI at some stage and 58 % to screen CVs; only 35 % always tell the candidate.
Sources: [Resume Builder](https://resumebuilder.com/7-in-10-companies-will-use-ai-in-the-hiring-process-in-2025-despite-most-saying-its-biased/) · [Resume Genius, Jul 2026](https://resumegenius.com/blog/ai-impact-on-hiring-2026) — Vendor.

**Companies and candidates see it very differently.** 70 % of hiring managers say AI hires faster and better; only 8 % of candidates see it as fair. Only 21 % of recruiters are very confident their system does not screen out qualified people (4,136 people in the US, UK, Ireland and Germany).
Source: [Greenhouse, Nov 2025](https://www.greenhouse.com/newsroom/an-ai-trust-crisis-70-of-hiring-managers-trust-ai-to-make-faster-and-better-hiring-decisions-only-8-of-job-seekers-call-it-fair) — Vendor.

## 2.2 LinkedIn: how its agent finds you

**LinkedIn's Hiring Assistant has been available worldwide (in English) since September 2025.** LinkedIn says it saves more than 4 hours per role and that recruiters review 62 % fewer profiles.
Source: [LinkedIn News](https://news.linkedin.com/2025/hiring-assistant-globally-available) — Vendor.

**How it works, according to LinkedIn's engineers:**
1. The recruiter's request (a job post, notes, even the CV of someone who is leaving) becomes a list of requirements.
2. An agent searches the profile index in parallel.
3. Smaller models review each candidate's **profile and CV** for evidence of each requirement, and quote the exact text.
→ **Implication:** if a requirement is not written in your profile or CV, there is no evidence to quote.
Source: [InfoQ, QCon 2025 talk](https://www.infoq.com/presentations/LinkedIn-agent-hiring-assistant/) — Primary.

**The ranking:** more than 1 billion profiles turned into meaning vectors; filters by title, seniority, location and requirements; a ranking with more than 100 signals; and a model that judges fit and writes the explanation. **Profiles that change are reprocessed every day.** Exact-keyword search found nothing for half the queries that meaning-based search could answer.
Sources: [ZenML on LinkedIn](https://www.zenml.io/llmops-database/semantic-search-for-ai-agents-at-scale-retrieval-and-ranking-for-linkedins-hiring-assistant) · [arXiv 2602.07309](https://arxiv.org/abs/2602.07309v1) — Primary.

**LinkedIn also infers skills** from titles and education (more than 41,000 skills), and downweights generic ones such as "Microsoft Word".
Source: [LinkedIn Economic Graph, Mar 2025](https://economicgraph.linkedin.com/content/dam/me/economicgraph/en-us/PDF/skills-based-hiring-march-2025.pdf) — Primary.

**Open to Work:** turning it on doubled the chance of getting recruiter messages, but that figure is from 2020. No 2025–26 evidence was found on whether it affects the agent.
Source: [LinkedIn Blog, 2020](https://blog.linkedin.com/2020/october/29/the-benefits-of-sharing-with-your-community-you-re-open-to-work) — Vendor, old.

**LinkedIn has verified more than 100 million people.** Verified members get up to 60 % more profile views.
Source: [LinkedIn News, Dec 2025](https://news.linkedin.com/2025/verified--linkedin-crosses-100m-member-milestone) — Vendor.
→ **What to do:** keep the profile complete (title, skills, experience with achievements, location), verified and consistent with the CV.

**Other agents:** Workday bought Paradox (a conversational agent for applying and scheduling, Oct 2025). Indeed launched Career Scout (for candidates) and Talent Scout (searches 615 million profiles for employers).
Sources: [Workday](https://newsroom.workday.com/2025-10-01-Workday-Completes-Acquisition-of-Paradox) · [Indeed](https://www.indeed.com/news/releases/indeed-introduces-new-suite-of-hiring-products-career-scout-talent-scout-premium-sponsored-jobs-and-indeed-connect?co=US) — Vendor.

## 2.3 How language models read CVs (studies)

**They show name bias.** In more than 3 million comparisons across three models, names associated with white people were preferred 85 % of the time versus 9 % for names associated with Black people.
Source: [University of Washington, 2024](https://www.washington.edu/news/2024/10/31/ai-bias-resume-screening-race-gender/) — Primary.

**They prefer the first candidate in the list** (63.5 % versus 36.5 %, in 21 of 22 models). In the same study, gender bias went the opposite way from the Washington study: results depend on the model.
Source: [Rozado, arXiv 2025](https://arxiv.org/abs/2505.17049v2) — Primary.

**Changing the presentation without changing qualifications flips decisions:** 30 % to 41 % of comparisons changed when the same CV was rewritten, reordered or polished, or depending on how cleanly its text was extracted.
Source: [Chen and Xiao, arXiv Sep 2026](https://arxiv.org/abs/2609.16517) — Primary (small models).
→ **Implication:** form matters more with AI than with people. Write clearly and make sure the text extracts cleanly.

**Many models do not pick the most qualified candidate well.**
Source: [Princeton, arXiv Feb 2026](https://arxiv.org/abs/2602.18550) — Primary.

**Models prefer text written by models.** GPT-3.5, GPT-4 and others chose options described by AI over ones written by people (tested with products and articles, not CVs).
Source: [PNAS, Aug 2025](https://ideas.repec.org/a/nas/journl/v122y2025pe2415697122.html) — Primary.

## 2.4 Candidates use AI too

**About 4 in 10 candidates use AI when applying** (54 % for the CV, 50 % for the cover letter). Only 26 % trust AI to evaluate them fairly.
Source: [Gartner, Jul 2025](https://www.gartner.com/en/newsroom/press-releases/2025-07-31-gartner-survey-shows-just-26-percent-of-job-applicants-trust-ai-will-fairly-evaluate-them) — Primary.

**About 1 in 5 managers would reject an AI-written CV, and almost nobody can spot one.** 52 % accept AI for drafting or editing; in a test, they identified the AI CV only a third of the time. OpenAI withdrew its own AI-text detector in 2023 for low accuracy.
Sources: [TopResume, Jun 2025](https://topresume.com/career-advice/ai-in-hiring-survey) — Vendor · [OpenAI](https://openai.com/index/new-ai-classifier-for-indicating-ai-written-text/) — Primary.

**Auto-apply bots:** they exist (one applied to about 1,000 roles in 2 days), but LinkedIn blocks them and restricts accounts. Greenhouse Real Talent flags bots and mass applications.
Sources: [Semafor](https://semafor.com/article/09/12/2024/linkedins-have-nots-and-have-bots) — Anecdotal · [Greenhouse Real Talent](https://www.greenhouse.com/blog/introducing-greenhouse-real-talent) — Vendor.

**Hidden text to trick the AI:** in real data, only about 1 % of roughly 200,000 CVs had it. Converted to plain text, it becomes visible to the recruiter, and systems with defenses block the attacks. One survey says 41 % "admit" to it, but that figure is almost certainly inflated by how the question was understood.
Sources: [arXiv 2605.28999](https://arxiv.org/abs/2605.28999) · [arXiv 2512.20164](https://arxiv.org/abs/2512.20164) — Primary · [Built In](https://builtin.com/articles/hidden-ai-prompts-in-resume) — Anecdotal.
→ **What to do:** never. It does not work, and it gets you discarded.

## 2.5 Fraud and identity

**Gartner predicts that 1 in 4 candidate profiles worldwide will be fake by 2028.** 6 % of candidates admitted to interview fraud.
Source: [Gartner](https://www.gartner.com/en/newsroom/press-releases/2025-07-31-gartner-survey-shows-just-26-percent-of-job-applicants-trust-ai-will-fairly-evaluate-them) — Primary.

**Fake remote workers placed by North Korea** at more than 100 US companies using stolen identities. Companies now ask for on-camera identity checks and ship equipment only to verified addresses.
Sources: [DOJ, Jun 2025](https://www.justice.gov/opa/pr/justice-department-announces-coordinated-nationwide-actions-combat-north-korean-remote) — Primary · [Holland & Knight, Aug 2026](https://www.hklaw.com/en/insights/publications/2026/08/hidden-in-plain-sight-labor-employment-and-cybersecurity-risks).
→ **Implication for remote candidates in Latin America:** expect identity checks. A verified LinkedIn profile and consistent data help you not look suspicious.

## 2.6 Laws that regulate AI in hiring

| Where | What it says | Since |
|---|---|---|
| New York City (Local Law 144) | Annual bias audit and notice to the candidate 10 business days in advance. Little real enforcement: 2 complaints in 2 years. | Jul 2023 · [NYC](https://www.nyc.gov/site/dca/about/automated-employment-decision-tools.page) · [state audit](https://www.osc.ny.gov/state-agencies/audits/2025/12/02/enforcement-local-law-144-automated-employment-decision-tools) |
| European Union (AI Act) | AI for hiring is "high risk". Already banned: AI that infers emotions at work. High-risk obligations were **postponed to 2 Dec 2027**. | Feb 2025 / Dec 2027 · [Annex III](https://artificialintelligenceact.eu/annex/3/) · [Gibson Dunn](https://www.gibsondunn.com/eu-ai-act-omnibus-agreement-postponed-high-risk-deadlines-and-other-key-changes/) |
| Colorado | The original law never took effect. A new one replaced it: notice when AI is used and an explanation within 30 days after an adverse outcome. | Jan 2027 · [McDermott](https://www.mcdermottlaw.com/insights/colorado-ai-law-in-flux-comprehensive-replacement-bill-signed-after-federal-court-blocks-predecessors-enforcement/) |
| Illinois | Bans discriminatory use of AI in employment and requires notice. The detailed rules were withdrawn in Jun 2026. | Jan 2026 · [Burke Warren](https://www.burkelaw.com/alert-illinois-department-of-human-rights-withdraws-proposed-ai-in-employment-rules) |
| California | Civil rights rules for automated systems (Oct 2025). Privacy rules with notice, access to the logic and appeal (Jan 2027). | [Mayer Brown](https://www.mayerbrown.com/en/insights/publications/2025/08/california-adopts-new-employment-ai-regulations-effective-october-1-2025) · [Littler](https://littler.com/news-analysis/asap/californias-long-awaited-final-regulations-automated-decisionmaking-create-new) |
| US federal | EEOC and DOL guidance on AI was withdrawn in 2025, but anti-discrimination laws still apply. | [Cooley](https://www.cooley.com/news/insight/2025/2025-02-21-gone-but-not-forgotten-federal-laws-still-apply-despite-guidance-disappearance-act) |
| Peru | AI used to select or evaluate workers is high risk; human oversight is mandatory. | Sep 2025 · [RSM](https://www.rsm.global/peru/en/node/1618) |
| Brazil | A bill passed the Senate and is pending in the Chamber of Deputies. Not law yet. | [CASRAI](https://casrai.org/guides/brazil-ai-bill-pl-2338-status) |
| Costa Rica | Three AI bills under discussion; none is law, and none deals specifically with employment. | [El Financiero, Mar 2025](https://www.elfinancierocr.com/tecnologia/que-plantean-tres-proyectos-de-ley-sobre/ZT3GKQ3YZ5AQBNN64NLIZNDDZE/story/) |

**Ongoing lawsuits:** Mobley v. Workday (age discrimination, a nationwide collective action since May 2025 that includes people graded by HiredScore), and a suit against Eightfold AI (Jan 2026) over profiles built from data collected without notice.
Sources: [Holland & Knight](https://www.hklaw.com/en/insights/publications/2025/05/federal-court-allows-collective-action-lawsuit-over-alleged) · [Epstein Becker Green](https://www.ebglaw.com/workforce-bulletin/ai-hiring-tools-and-consumer-reports-understanding-the-eightfold-litigation).
→ **For candidates:** in some places you have the right to be notified, to ask for an explanation or to ask for human review. Ashby, for example, lets you opt out of AI evaluation.

## 2.7 Machine-readable profiles

**No ATS documents reading JSON Resume or Schema.org data.** ATS read the uploaded file or the form fields.
Source: [JSON Resume](https://jsonresume.org/) — inferred from the documentation reviewed.

**They do help with search engines and agents that browse the web.** Schema.org has types for occupation, skills and qualifications, and Google uses profile data in search.
Sources: [Schema.org Occupation](https://schema.org/Occupation) · [Google](https://developers.google.com/search/docs/appearance/structured-data/profile-page) — Primary.
→ **What to do:** an optional extra for people with a personal website. It does not replace the CV or LinkedIn.

## Summary: what a CV needs for AI screening

1. Every requirement written in plain text, with evidence (LinkedIn, Ashby and HiredScore check requirement by requirement).
2. A file that parses cleanly (no readable CV means no grade, and text quality changes the decision).
3. A complete, verified, up-to-date LinkedIn profile (it is reprocessed daily).
4. Nothing hidden.
5. Some noise cannot be controlled (order, bias), so applying well to more postings is worth more than perfecting a single one.
