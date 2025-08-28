from flask import Blueprint, jsonify, request
from services.downloader import download_invoice
from services.parser import parse_invoice
from models.invoice_model import save_parsed_invoice, get_all_parsed, get_summary, get_high_value, parsed_invoice_by_ticket
from pathlib import Path
import os

invoice_bp = Blueprint("invoice_bp", __name__)
BASE_DIR = Path(__file__).resolve().parent.parent
INVOICES_DIR = BASE_DIR / "invoices"

@invoice_bp.route("/download/<ticket_number>", methods=["POST"])
def download(ticket_number):
    """
    Generate/download a PDF for ticket_number (simulated).
    Returns 200 on created, 500 on failure.
    """
    try:
        pdf_path = download_invoice(ticket_number)
        pdf_url = f"/invoices/{pdf_path.name}"
        return jsonify({"status": "Downloaded", "pdf_path": pdf_url}), 200
    except Exception as e:
        return jsonify({"status": "Error", "message": str(e)}), 500

@invoice_bp.route("/parse/<ticket_number>", methods=["POST"])
def parse(ticket_number):
    """
    Parse the PDF for a ticket and store structured data.
    """
    pdf_file = INVOICES_DIR / f"{ticket_number}.pdf"
    if not pdf_file.exists():
        return jsonify({"status": "File Not Found"}), 404
    parsed = parse_invoice(str(pdf_file))
    # attach ticket and pdf url
    parsed_record = {
        "ticket_number": ticket_number,
        "pdf_url": f"/invoices/{pdf_file.name}",
        **parsed
    }
    save_parsed_invoice(parsed_record)
    return jsonify(parsed_record), 200

@invoice_bp.route("/", methods=["GET"])
def list_parsed():
    """
    Return all parsed invoices.
    """
    return jsonify(get_all_parsed())

@invoice_bp.route("/summary", methods=["GET"])
def summary():
    return jsonify(get_summary())

@invoice_bp.route("/high-value", methods=["GET"])
def high_value():
    try:
        threshold = float(request.args.get("threshold", "10000"))
    except:
        threshold = 10000.0
    return jsonify(get_high_value(threshold))

@invoice_bp.route("/ticket/<ticket_number>", methods=["GET"])
def get_by_ticket(ticket_number):
    rec = parsed_invoice_by_ticket(ticket_number)
    if not rec:
        return jsonify({"status": "Not Found"}), 404
    return jsonify(rec)
