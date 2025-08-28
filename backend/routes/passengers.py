from flask import Blueprint, jsonify
import json
from pathlib import Path
from models.invoice_model import invoice_exists, parsed_invoice_by_ticket

passenger_bp = Blueprint("passenger_bp", __name__)
BASE_DIR = Path(__file__).resolve().parent.parent

@passenger_bp.route("/", methods=["GET"])
def get_passengers():
    """
    Returns passenger JSON with computed Download/Parse statuses.
    """
    data_path = BASE_DIR / "data" / "passenger_data.json"
    with open(data_path, "r", encoding="utf-8") as f:
        passengers = json.load(f)

    # augment with statuses
    augmented = []
    for p in passengers:
        ticket = p.get("ticket_number")
        download_status = "Downloaded" if invoice_exists(ticket) else "Pending"
        parse_status = "Parsed" if parsed_invoice_by_ticket(ticket) else "Pending"
        augmented.append({
            **p,
            "download_status": download_status,
            "parse_status": parse_status
        })
    return jsonify(augmented)
