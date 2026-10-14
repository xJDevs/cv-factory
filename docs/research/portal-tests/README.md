Part of CV Factory by Johel Gomez Rojas — Apache License 2.0.

# Autofill test on real job portals (October 2026)

The fictional CV of Ana María Solís Vargas (the engine's example output, `engine/example/output/`) was uploaded to real application forms. **Nothing was submitted.**

| Portal | Result |
|---|---|
| Lever (Palantir) | Filled in name, email, location ("Heredia, CRI"), current company (correctly separated from the city) and LinkedIn. Phone without the "+": "50688880000". |
| Ashby (Ramp) | Saved the file and said "Autofill completed!", but left every field empty. It is unclear whether the cause is the PDF or that portal: it still needs testing with the DOCX and with the control PDF. |
| Greenhouse (GitLab) | That form does not fill fields from the CV; it only stores the file. |
| Workday | Not tested: it requires creating an account for each company. |

**Takeaway:** fields that come out wrong are fixed by hand when applying. Always review the form fields before submitting.

`Ana-Maria-Solis-Vargas-Resume-control.pdf` is the same CV generated from the DOCX with LibreOffice, used to check whether a portal is failing.
