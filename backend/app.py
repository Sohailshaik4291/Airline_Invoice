import os
from flask import Flask, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()  # loads .env if present

# ensure directories exist
BASE_DIR = Path(__file__).resolve().parent
(Path(BASE_DIR / "invoices")).mkdir(parents=True, exist_ok=True)
(Path(BASE_DIR / "parsed_data")).mkdir(parents=True, exist_ok=True)

app = Flask(__name__, static_folder=None)
CORS(app)

# register routes
from routes.passengers import passenger_bp
from routes.invoices import invoice_bp

app.register_blueprint(passenger_bp, url_prefix="/api/passengers")
app.register_blueprint(invoice_bp, url_prefix="/api/invoices")

# simple PDF serving (so frontend can open PDF URL)
@app.route("/invoices/<path:filename>")
def serve_invoice(filename):
    return send_from_directory(os.path.join(BASE_DIR, "invoices"), filename)

if __name__ == "__main__":
    debug = os.getenv("FLASK_DEBUG", "1") == "1"
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=debug)
