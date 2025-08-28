import os
import shutil
from models.invoice_story import store

def download_invoice(pid):
    passenger = next((p for p in store["passengers"] if p["id"] == pid), None)
    if not passenger:
        return {"status": "error", "message": "Passenger not found"}

    # Simulate invoice download → assume PDF is already in sample_invoices/
    src = f"backend/data/sample_invoices/{pid}.pdf"
    dest = f"backend/data/invoices/{pid}.pdf"
    if os.path.exists(src):
        shutil.copy(src, dest)
        passenger["download_status"] = "success"
        passenger["pdf_path"] = dest
    else:
        passenger["download_status"] = "not_found"
    return passenger
