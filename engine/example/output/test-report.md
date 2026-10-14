# Test report — 2026-10-13 22:44

**Result: APPROVED — ready to deliver**

## ✅ Pre-check: Complete data and allowed characters

## ✅ Pre-check: Traceability to the source data (confirmed facts only)
- complete reading: experience 4, achievements 6, skills 6 rows, all opened and read
- 21 references to the source data checked (read at fictional example)

## ✅ Test 1: Fonts embedded, with Unicode, no Type 3
- 2 fonts checked

## ✅ Test 2: Extraction with pdftotext, pdfminer, pdf.js and pdfium
- pdftotext: 100.0 %
- pdfminer: 100.0 %
- pdf.js: 100.0 %
- pdfium: 100.0 %

## ✅ Test 3: No spaced-out letters or split words
- 4 readers checked

## ✅ Test 4: Reading order and title–company–dates association
- 4 entries and 6 sections in order in the 4 readers

## ✅ Test 5: OpenResume parser (name, contact, jobs, education)
- phone outside the US: OpenResume only recognizes 10-digit US numbers; the phone is checked in tests 4 and 6
- sections detected: profile, PROFESSIONAL SUMMARY, SKILLS, PROFESSIONAL EXPERIENCE, EDUCATION, CERTIFICATIONS, LANGUAGES

## ✅ Test 6: AI extraction (agent without context, from PDF and from text)
- both agents extracted name, contact, jobs, education and languages without errors

## ✅ Test 7: Metadata, size and pages
- size 34 KB
- 1 page(s)
- tagged PDF

## ✅ Test 8: Clean, convertible DOCX
- bullets checked in 1 list(s)
- complete text through both paths (100.0 %)
- DOCX→PDF 4 fonts checked
- DOCX→PDF pdftotext: 100.0 %
- DOCX→PDF pdfminer: 100.0 %
- DOCX→PDF pdf.js: 100.0 %
- DOCX→PDF pdfium: 100.0 %

## ✅ Test 9: English CV without accents or ñ
- no accented letters or ñ in the PDF, the DOCX, the metadata or the file name
