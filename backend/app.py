from flask import Flask, jsonify, request
from flask_cors import CORS
import os
from services.downloader import download_invoice
from services.parser import parse_invoice
from models.invoice_story import store, get_all_invoices, get_summary

app = Flask(__name__)
CORS(app)

@app.route("/passengers", methods=["GET"])
def get_passengers():
    return jsonify(store["passengers"])

@app.route("/download/<int:pid>", methods=["POST"])
def download(pid):
    result = download_invoice(pid)
    return jsonify(result)

@app.route("/parse/<int:pid>", methods=["POST"])
def parse(pid):
    result = parse_invoice(pid)
    return jsonify(result)

@app.route("/invoices", methods=["GET"])
def invoices():
    return jsonify(get_all_invoices())

@app.route("/summary", methods=["GET"])
def summary():
    return jsonify(get_summary())

if __name__ == "__main__":
    app.run(debug=True)
