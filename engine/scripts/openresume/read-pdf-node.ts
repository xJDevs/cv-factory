// Copyright 2026 Johel Gomez Rojas. Part of CV Factory. Licensed under the Apache License, Version 2.0 (see LICENSE and NOTICE at the project root). Do not remove this notice.
// Node version of OpenResume's step 1 (read-pdf.ts), written for this engine.
// It does the same as the original: reads the text items with pdf.js, keeps x/y and the
// real font name (which OpenResume uses to detect bold text), and drops empty spaces.
// Only difference: it strips accents, because OpenResume only recognizes names in English letters
// (a limitation of the parser, not of the CV). That way the test measures the layout, not the language.
import { pathToFileURL } from "node:url";

type Item = { text: string; x: number; y: number; width: number; height: number; fontName: string; hasEOL: boolean };

const stripAccents = (t: string) => t.normalize("NFD").replace(/[̀-ͯ]/g, "");

export const readPdf = async (pdfPath: string): Promise<Item[]> => {
  const root = process.env.PDFJS_ROOT as string;
  const pdfjs: any = await import(pathToFileURL(`${root}/legacy/build/pdf.mjs`).href);
  const pdf = await pdfjs.getDocument({ url: pathToFileURL(pdfPath), useSystemFonts: false, verbosity: 0 }).promise;
  let items: Item[] = [];
  for (let i = 1; i <= pdf.numPages; i++) {
    const page = await pdf.getPage(i);
    const content = await page.getTextContent();
    await page.getOperatorList();
    const common = page.commonObjs;
    for (const it of content.items as any[]) {
      if (!("str" in it)) continue;
      const { str, dir, transform, fontName, ...rest } = it;
      const font = common.get(fontName);
      items.push({ ...rest, fontName: font?.name ?? fontName, text: stripAccents(str.replace(/-­‐/g, "-")),
                   x: transform[4], y: transform[5] });
    }
  }
  return items.filter((t) => t.hasEOL || t.text.trim() !== "");
};
