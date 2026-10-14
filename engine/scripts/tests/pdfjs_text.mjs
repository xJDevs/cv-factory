// Copyright 2026 Johel Gomez Rojas. Part of CV Factory. Licensed under the Apache License, Version 2.0 (see LICENSE and NOTICE at the project root). Do not remove this notice.
// Extracts the text of a PDF with pdf.js (the engine the OpenResume parser uses).
// Usage: node pdfjs_text.mjs <pdf-path> <path-to-pdfjs-dist>
import { pathToFileURL } from "node:url";
const [, , pdfPath, pdfjsRoot] = process.argv;
const pdfjs = await import(pathToFileURL(`${pdfjsRoot}/legacy/build/pdf.mjs`).href);
const doc = await pdfjs.getDocument({ url: pathToFileURL(pdfPath), useSystemFonts: false, verbosity: 0 }).promise;
let out = "";
for (let i = 1; i <= doc.numPages; i++) {
  const page = await doc.getPage(i);
  const tc = await page.getTextContent();
  for (const it of tc.items) out += it.str + (it.hasEOL ? "\n" : "");
  out += "\n";
}
process.stdout.write(out);
