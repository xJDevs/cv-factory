import * as pdfjs from '/home/claude/.npm-global/lib/node_modules/pdfjs-dist/legacy/build/pdf.mjs';
const doc = await pdfjs.getDocument({url: process.argv[2], useSystemFonts: false}).promise;
const page = await doc.getPage(1);
const tc = await page.getTextContent();
let out = '';
for (const it of tc.items) { out += it.str + (it.hasEOL ? '\n' : '|'); }
console.log(JSON.stringify(out));
