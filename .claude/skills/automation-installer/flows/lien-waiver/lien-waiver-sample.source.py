from reportlab.lib.pagesizes import LETTER
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
import sys, textwrap

OUT = sys.argv[1]
W, H = LETTER
L, R = 0.9*inch, W - 0.9*inch
c = canvas.Canvas(OUT, pagesize=LETTER)
c.setTitle("Conditional Waiver and Release on Final Payment")
y = H - 0.9*inch

def rule(yy, w=1.1):
    c.setLineWidth(w); c.line(L, yy, R, yy)

def centered(txt, size, bold, gap):
    global y
    c.setFont("Helvetica-Bold" if bold else "Helvetica", size)
    c.drawCentredString(W/2, y, txt); y -= gap

def para(txt, size=9.2, lead=12.2, width=104):
    global y
    c.setFont("Helvetica", size)
    for line in textwrap.wrap(txt, width):
        c.drawString(L, y, line); y -= lead
    y -= 2

def bold_block(txt, size=10, lead=13.5, width=88):
    global y
    c.setFont("Helvetica-Bold", size)
    for line in textwrap.wrap(txt, width):
        c.drawString(L, y, line); y -= lead

def field(label, gap=23, prefix=""):
    """A labeled blank. The underline is where the DocuSign field goes."""
    global y
    c.setFont("Helvetica", 10.5)
    c.drawString(L, y, label)
    lw = c.stringWidth(label, "Helvetica", 10.5)
    x0 = L + lw + 4
    if prefix:
        c.drawString(x0, y, prefix); x0 += c.stringWidth(prefix, "Helvetica", 10.5) + 2
    c.setLineWidth(0.6); c.line(x0, y - 2.5, R, y - 2.5)
    y -= gap

def section(title):
    global y
    y -= 4; rule(y); y -= 15
    centered(title, 11.5, True, 6)
    rule(y + 1, 0.6); y -= 15

# ---- title + notice -------------------------------------------------------
centered("CONDITIONAL WAIVER AND RELEASE ON FINAL PAYMENT", 13, True, 24)
bold_block("NOTICE: THIS DOCUMENT WAIVES THE CLAIMANT'S LIEN, STOP PAYMENT NOTICE, AND "
           "PAYMENT BOND RIGHTS EFFECTIVE ON RECEIPT OF PAYMENT. A PERSON SHOULD NOT RELY "
           "ON THIS DOCUMENT UNLESS SATISFIED THAT THE CLAIMANT HAS RECEIVED PAYMENT.")
y -= 10

# ---- identifying information ---------------------------------------------
section("Identifying Information")
field("Name of Claimant:")
field("Name of Customer:")
field("Job Location:")
field("Owner:")
y -= 6; rule(y); y -= 20

# ---- the release ----------------------------------------------------------
centered("Conditional Waiver and Release", 11.5, True, 16)
para("This document waives and releases the lien, stop payment notice and payment bond "
     "rights the claimant has for labor and service provided, and for equipment and "
     "material delivered, to the customer on this job through the Through Date shown "
     "below. Rights arising from labor or service provided, or equipment or material "
     "delivered, under a written change order fully executed by the parties before the "
     "date this document is signed by the claimant are waived and released by this "
     "document, unless they are listed as an Exception below. This document takes effect "
     "only when the claimant has received payment from the financial institution on which "
     "the following check is drawn.")
y -= 8
field("Maker of Check:")
field("Amount of Check:", prefix="$")
field("Check Payable To:")
field("Through Date:")
y -= 4; rule(y); y -= 20

# ---- exceptions -----------------------------------------------------------
centered("Exceptions", 11.5, True, 16)
para("This document does not affect any of the following:")
y -= 4
c.setLineWidth(0.6); c.line(L, y, R, y); y -= 26
rule(y); y -= 20

# ---- signature ------------------------------------------------------------
centered("Signature", 11.5, True, 16)
field("Claimant's Signature:", gap=30)
field("Claimant's Title:")
field("Date of Signature:")

# ---- footer ---------------------------------------------------------------
c.setFont("Helvetica-Oblique", 7.6)
c.drawString(L, 0.72*inch,
    "Sample form supplied with the VA Optional lien waiver automation. Lien waiver "
    "requirements are set by state and this is not legal advice —")
c.drawString(L, 0.72*inch - 10,
    "have your attorney confirm the correct form for the state your property is in before you use it.")
c.showPage(); c.save()
print("wrote", OUT)
