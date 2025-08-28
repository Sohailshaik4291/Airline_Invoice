import os
import json
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "").strip()
USE_MONGO = bool(MONGO_URI)

# JSON fallback
BASE_DIR = Path(__file__).resolve().parent.parent
PARSED_JSON = BASE_DIR / "parsed_data" / "invoices.json"
PARSED_JSON.parent.mkdir(parents=True, exist_ok=True)
if not PARSED_JSON.exists():
    PARSED_JSON.write_text("[]", encoding="utf-8")

if USE_MONGO:
    from pymongo import MongoClient
    client = MongoClient(MONGO_URI)
    db = client.get_database()  # default DB from URI
    invoices_coll = db.get_collection("invoices")
else:
    invoices_coll = None

def _read_json_all():
    with open(PARSED_JSON, "r", encoding="utf-8") as f:
        return json.load(f)

def _write_json_all(arr):
    with open(PARSED_JSON, "w", encoding="utf-8") as f:
        json.dump(arr, f, indent=2)

def save_parsed_invoice(record: dict):
    """
    Upsert by ticket_number. record must contain ticket_number.
    """
    if USE_MONGO:
        invoices_coll.update_one({"ticket_number": record["ticket_number"]}, {"$set": record}, upsert=True)
    else:
        arr = _read_json_all()
        found = False
        for i, r in enumerate(arr):
            if r.get("ticket_number") == record.get("ticket_number"):
                arr[i] = record
                found = True
                break
        if not found:
            arr.append(record)
        _write_json_all(arr)

def get_all_parsed():
    if USE_MONGO:
        docs = list(invoices_coll.find({}, {"_id": 0}))
        return docs
    else:
        return _read_json_all()

def parsed_invoice_by_ticket(ticket_number: str):
    if USE_MONGO:
        doc = invoices_coll.find_one({"ticket_number": ticket_number}, {"_id": 0})
        return doc
    else:
        arr = _read_json_all()
        for r in arr:
            if r.get("ticket_number") == ticket_number:
                return r
        return None

def get_summary():
    """
    Returns airline-wise totals and counts:
    { "Indigo": {"total_amount": 12345.0, "count": 2}, ... }
    """
    summary = {}
    arr = get_all_parsed()
    for r in arr:
        airline = r.get("airline") or "Unknown"
        amt = r.get("amount") or 0
        summary.setdefault(airline, {"total_amount": 0.0, "count": 0})
        try:
            summary[airline]["total_amount"] += float(amt)
        except:
            pass
        summary[airline]["count"] += 1
    return summary

def get_high_value(threshold: float):
    res = []
    arr = get_all_parsed()
    for r in arr:
        amt = r.get("amount")
        try:
            if amt is not None and float(amt) > threshold:
                res.append(r)
        except:
            continue
    return res

def invoice_exists(ticket_number: str) -> bool:
    """
    Check if invoice PDF exists on disk.
    """
    pdf = BASE_DIR / "invoices" / f"{ticket_number}.pdf"
    return pdf.exists()
