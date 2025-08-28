store = {
    "passengers": [
        {"id": 1, "name": "John Doe", "download_status": "pending", "parse_status": "pending"},
        {"id": 2, "name": "Alice Smith", "download_status": "pending", "parse_status": "pending"},
        {"id": 3, "name": "Sohail", "download_status": "pending", "parse_status": "pending"}
    ],
    "invoices": []
}

def get_all_invoices():
    return store["invoices"]

def get_summary():
    summary = {}
    for inv in store["invoices"]:
        airline = inv["airline"]
        summary[airline] = summary.get(airline, 0) + inv["amount"]
    return summary
