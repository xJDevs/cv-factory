# Instructions for the test 6 agent

Test 6 checks the CV the way an AI reader sees it. The main agent starts **two agents with no context at all** about the person or the CV:

1. One gets the PDF file (so it sees the CV the way an AI reader with image and text would).
2. The other gets only the `plain-text.txt` file from the output folder (what a system that only uses the extracted text sees).

Send each one **only the block below**, and fill in its two blanks: the file it must read, and the path where it must write its answer (`<output folder>/ai-from-pdf.json` for agent 1, `<output folder>/ai-from-text.json` for agent 2). Send nothing else: no tests, no grading, nothing about the person.

## Prompt to send (copy only this block)

```text
You are a recruiting system. Read the resume in this file: <FILE TO READ>

Extract its data exactly as written, without correcting, completing or inventing anything. If a piece of data does not appear, leave it empty. Use this JSON:

{
  "name": "",
  "headline": "",
  "email": "",
  "phone": "",
  "location": "",
  "linkedin": "",
  "experience": [{"title": "", "company": "", "dates": ""}],
  "education": [{"degree": "", "institution": "", "dates": ""}],
  "certifications": [{"name": "", "issuer": ""}],
  "languages": [{"language": "", "level": ""}]
}

In "dates", copy the range exactly as written, in the resume's own language (for example "October 2025 – Present" or "octubre 2025 – Actualidad").

Write only that JSON, as UTF-8, to this file: <OUTPUT PATH>
```

## For the main agent only — do not send

`cv.py generate` deletes both files, because they are no longer valid for a newly generated PDF. When both agents have written their files, run `cv.py test`.

What test 6 compares:

- `name` and `email`: equal to the CV (ignoring case and extra spaces).
- `phone`: same digits as the CV (if the CV has a phone).
- `experience`: same number of jobs, and each `title`, `company` and `dates` equal to the CV, in order.
- `education`: each `institution` contains the CV's institution, in order.
- `languages`: every language of the CV appears.

The other fields (`headline`, `location`, `linkedin`, education `dates`, `certifications`, `level`) are requested so the agent reads the whole CV, but they are not compared.
