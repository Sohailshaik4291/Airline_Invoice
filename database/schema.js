import mongoose from "mongoose";

const invoiceSchema = new mongoose.Schema({
  ticket_number: String,
  invoice_no: String,
  date: String,
  airline: String,
  amount: Number,
  gstin: String,
  status: String
});

export default mongoose.model("Invoice", invoiceSchema);
