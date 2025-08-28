import pdfplumber
from models.invoice_story import store

def parse_invoice(pid):
    passenger = next((p for p in store["passengers"] if p["id"] == pid), None)
    if not passenger or passenger.get("download_status") != "success":
        return {"status": "error", "message": "Invoice not available"}

    pdf_path = passenger["pdf_path"]
    try:
        with pdfplumber.open(pdf_path) as pdf:
            text = ""
            for page in pdf.pages:
                text += page.extract_text()

        # Dummy extraction: you’d regex in real life
        invoice = {
            "invoice_no": "INV-" + str(pid),
            "date": "2025-08-28",
            "airline": "Indigo Airlines",
            "amount": 4500 + pid,
            "gstin": "29ABCDE1234F2Z5",
            "status": "parsed"
        }

        passenger["parse_status"] = "success"
        passenger["invoice"] = invoice
        store["invoices"].append(invoice)
        return invoice
    except Exception as e:
        passenger["parse_status"] = "error"
        return {"status": "error", "message": str(e)}
