from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Preformatted, PageBreak
)
from reportlab.lib.enums import TA_LEFT
import os

BASE = os.path.dirname(__file__)

FILES = [
    ("paint/01.py", "Paint — 01: Mouse Events"),
    ("paint/02.py", "Paint — 02: Freehand Lines"),
    ("paint/03.py", "Paint — 03: Rectangle Tool"),
    ("paint/04.py", "Paint — 04: Rubber-band Preview (base_layer)"),
    ("01.py",       "Sprites — 01: Basic Sprite"),
    ("02.py",       "Sprites — 02: Sprite Groups"),
    ("03.py",       "Sprites — 03: Player and Enemy"),
    ("04.py",       "Sprites — 04: Collision Detection"),
    ("05.py",       "Sprites — 05: USEREVENT + kill()"),
    ("racer.py",    "Racer — Full Game Demo"),
]

doc = SimpleDocTemplate(
    os.path.join(BASE, "week11_examples.pdf"),
    pagesize=A4,
    leftMargin=1.5*cm, rightMargin=1.5*cm,
    topMargin=2*cm,    bottomMargin=2*cm,
)

styles = getSampleStyleSheet()

title_style = ParagraphStyle(
    "SectionTitle",
    parent=styles["Heading2"],
    fontSize=13,
    textColor=colors.HexColor("#1a1a6e"),
    spaceAfter=6,
)

code_style = ParagraphStyle(
    "Code",
    parent=styles["Code"],
    fontSize=7.5,
    leading=11,
    fontName="Courier",
    backColor=colors.HexColor("#f5f5f5"),
    borderColor=colors.HexColor("#cccccc"),
    borderWidth=0.5,
    borderPadding=6,
    leftIndent=0,
    rightIndent=0,
    wordWrap="CJK",
)

story = []

# Cover title
story.append(Spacer(1, 2*cm))
story.append(Paragraph("Week 11 — Pygame Examples", styles["Title"]))
story.append(Paragraph("Paint series &amp; Sprite / Racer demos", styles["Normal"]))
story.append(Spacer(1, 1*cm))

for rel_path, label in FILES:
    story.append(PageBreak())
    story.append(Paragraph(label, title_style))
    story.append(Spacer(1, 0.3*cm))

    src = open(os.path.join(BASE, rel_path)).read()
    story.append(Preformatted(src, code_style))

doc.build(story)
print("PDF written to week11_examples.pdf")
