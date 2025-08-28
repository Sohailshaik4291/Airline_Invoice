import pdfplumber
import re

def parse_invoice(pdf_path: str) -> dict:
    """
    Extract invoice_no, date, airline, amount, gstin from PDF text.
    Returns a dict. If a field not found, leaves empty or None.
    """
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for p in pdf.pages:
            page_text = p.extract_text()
            if page_text:
                text += page_text + "\n"

    # Patterns (be flexible)
    patterns = {
        "invoice_no": r"Invoice[:\s]*\s*(INV\d+|\d+)",
        "date": r"Date[:\s]*\s*([0-9]{4}-[0-9]{2}-[0-9]{2}|[0-9]{2}-[0-9]{2}-[0-9]{4})",
        "airline": r"Airline[:\s]*\s*([A-Za-z \-&]+)",
        "amount": r"Amount[:\s]*\s*([0-9]+(?:\.[0-9]{1,2})?)",
        "gstin": r"GSTIN[:\s]*\s*([A-Z0-9]{10,15})"
    }

    result = {}
    for k, pat in patterns.items():
        m = re.search(pat, text, re.IGNORECASE)
        if m:
            result[k] = m.group(1).strip()
        else:
            # fallback to None or empty
            result[k] = None

    # convert numeric
    if result.get("amount"):
        try:
            result["amount"] = float(result["amount"])
        except:
            result["amount"] = None

    # set status
    result["status"] = "Parsed"
    return result
