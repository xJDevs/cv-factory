import sys
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
c = canvas.Canvas(sys.argv[1], pagesize=letter)
c.setTitle("Jane Doe - Resume"); c.setAuthor("Jane Doe")
c.setFont("Helvetica", 11)
c.drawRightString(560, 700, "Jan 2020 – Present")   # drawn first
c.drawString(50, 700, "Senior Engineer, Acme Inc.")       # drawn second
c.drawString(50, 680, "• bullet  ★ star  ✓ check  office  “q”")
pdfmetrics.registerFont(TTFont("DejaVu", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"))
c.setFont("DejaVu", 11)
c.drawString(50, 660, "TTF: • bullet  ★ star  ✓ check  office")
t = c.beginText(50, 640); t.setFont("Helvetica", 11); t.setCharSpace(3); t.textLine("Tracked text Python"); c.drawText(t)
c.save()
