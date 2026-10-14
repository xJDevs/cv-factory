// Copyright 2026 Johel Gomez Rojas. Part of CV Factory. Licensed under the Apache License, Version 2.0 (see LICENSE and NOTICE at the project root). Do not remove this notice.
// Runs the OpenResume parser on a PDF and prints what it extracted, as JSON.
// Steps 2–4 are OpenResume's original code (AGPL-3.0), downloaded separately when the
// test runs; it is not distributed with this engine.
import { readPdf } from "./read-pdf-node";
import { groupTextItemsIntoLines } from "lib/parse-resume-from-pdf/group-text-items-into-lines";
import { groupLinesIntoSections } from "lib/parse-resume-from-pdf/group-lines-into-sections";
import { extractResumeFromSections } from "lib/parse-resume-from-pdf/extract-resume-from-sections";

async function main() {
  const items = await readPdf(process.argv[2]);
  const lines = groupTextItemsIntoLines(items as any);
  const sections = groupLinesIntoSections(lines);
  const result = extractResumeFromSections(sections);
  process.stdout.write(JSON.stringify({ sections: Object.keys(sections), result }, null, 2));
}
main();
