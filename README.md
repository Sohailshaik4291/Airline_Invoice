# ✈️ Airline Invoice App

A mini full-stack project for downloading, parsing, and visualizing airline invoices.  
Built as part of an **Internship Hackathon Assignment**.

---

## 📌 Problem Statement
- Download airline invoice PDFs using passenger data.  
- Extract key details from PDFs:
  - Invoice Number  
  - Date  
  - Airline  
  - Amount  
  - GSTIN (if available)  
- Display results in a dashboard with backend APIs.  

---

## 🛠️ Tech Stack
- **Frontend:** React, Axios  
- **Backend:** Flask (Python), Flask-CORS  
- **Database:** MongoDB *(optional, else JSON file storage)*  
- **PDF Parsing:** pdfplumber, regex  
- **PDF Generation (simulated invoices):** reportlab  

---




---

## 🚀 Getting Started

### 1️⃣ Backend Setup (Flask)
```bash
cd backend
python -m venv venv
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate

pip install -r requirements.txt

# run server
python app.py

# ---------------------------------
for fronted

cd frontend
npm install
npm start


## 📂 Fronted UI
Frontend Features

Passenger Records Table

Shows Download Status & Parse Status

Download & Parse actions per passenger

Invoices Table

Invoice No | Date | Airline | Amount | GSTIN | Status | PDF Link

Summary View

Airline-wise totals & invoice counts

Extras

Error badges

Refresh buttons

Flag for review (UI state only)




📡 API Endpoints
Method	Endpoint	Description
GET	/api/passengers/	List passenger records with download/parse status
POST	/api/invoices/download/:ticket_number	Download invoice PDF (simulated)
POST	/api/invoices/parse/:ticket_number	Parse invoice PDF and store structured data
GET	/api/invoices/	List all parsed invoices
GET	/api/invoices/summary	Airline-wise totals
GET	/api/invoices/high-value?threshold=10000	Invoices above threshold
GET	/invoices/:file.pdf	Serve raw PDF file
