import sys, subprocess
from pdfminer.high_level import extract_text
import pdfplumber, pypdfium2 as pdfium
p=sys.argv[1]
def show(name, t): print(f"--- {name}:\n{t.strip()}\n   repr-tail: {ascii(t.strip()[:400])}")
show("pdftotext", subprocess.run(["pdftotext",p,"-"],capture_output=True,text=True).stdout)
show("pdfminer", extract_text(p))
with pdfplumber.open(p) as pdf: show("pdfplumber", pdf.pages[0].extract_text() or "")
doc=pdfium.PdfDocument(p); show("pdfium", doc[0].get_textpage().get_text_range())
