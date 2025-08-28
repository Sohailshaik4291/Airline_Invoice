import random
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from datetime import date
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent
INVOICES_DIR = BASE_DIR / "invoices"
INVOICES_DIR.mkdir(parents=True, exist_ok=True)

AIRLINES = ["Indigo", "Air India", "Vistara", "SpiceJet", "GoAir", "Emirates"]

def generate_gstin():
    # simple fake GSTIN (not guaranteed valid) - 15 chars
    import string
    letters = string.ascii_uppercase + "0123456789"
    return "".join(random.choice(letters) for _ in range(15))

def download_invoice(ticket_number: str) -> Path:
    """
    Simulate downloading by generating a PDF with invoice fields.
    Returns Path to created PDF.
    """
    invoice_no = "INV" + ticket_number[-6:]
    today = date.today().isoformat()
    airline = random.choice(AIRLINES)
    # random amount between 500 and 25000
    amount = round(random.uniform(500, 25000), 2)
    # include GSTIN ~70% of time
    gstin = generate_gstin() if random.random() < 0.7 else ""

    filename = INVOICES_DIR / f"{ticket_number}.pdf"
    c = canvas.Canvas(str(filename), pagesize=A4)
    width, height = A4
    left = 80
    top = height - 80

    c.setFont("Helvetica-Bold", 14)
    c.drawString(left, top, f"Invoice: {invoice_no}")

    c.setFont("Helvetica", 11)
    y = top - 30
    c.drawString(left, y, f"Ticket Number: {ticket_number}")
    y -= 20
    c.drawString(left, y, f"Date: {today}")
    y -= 20
    c.drawString(left, y, f"Airline: {airline}")
    y -= 20
    c.drawString(left, y, f"Amount: {amount:.2f}")
    y -= 20
    if gstin:
        c.drawString(left, y, f"GSTIN: {gstin}")
    else:
        c.drawString(left, y, "GSTIN: N/A")

    # Add some footer / body text for robustness
    y -= 40
    c.setFont("Helvetica-Oblique", 9)
    c.drawString(left, y, "Thank you for choosing our airline. This is a system generated invoice.")
    c.showPage()
    c.save()

    return filename
