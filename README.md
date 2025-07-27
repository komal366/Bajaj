# 🤖 SmartQuery AI

**SmartQuery AI** is an AI-powered insurance query assistant that leverages NLP and Machine Learning to analyze user-submitted queries and PDF documents. It provides intelligent answers such as claim decisions, justification, estimated amount, matched clauses, and policy names — all in real time.

---

## 🚀 Features

- 🔐 User Login & Sign Up
- 🧾 Query Submission with Optional PDF Upload
- 🤖 AI-Powered Semantic Search from Policy Documents
- ✅ Decision Output: Approved / Rejected
- 💰 Estimated Claim Amount
- 📚 Justification + Matched Policy Clauses
- 🧠 Supports Custom Uploaded Documents
- 📂 Query & Upload History with View/Download

---

## 📦 Setup

```bash
git clone https://github.com/komal366/Bajaj.git
pip install -r requirements.txt
python app.py
```

📍 Open in browser: http://localhost:5000


### ⚙️ Tech Stack
💻 Frontend
HTML, TailwindCSS
JavaScript + Lucide Icons

### 🔙 Backend
Python (Flask)
MongoDB (PyMongo)
Sentence Transformers (MiniLM)
PyMuPDF (fitz) for PDF parsing

### 🧠 How It Works
🧾 User submits a query and optionally uploads a policy document.
📄 Clauses are extracted from PDF using regex-based chunking.
🤖 Query and clauses are encoded using Sentence-BERT (MiniLM).
🔍 Semantic similarity is computed between query and clauses.

### ✅ System returns:
Decision (Approved/Rejected)
Justification text
Matched clauses
Estimated amount

### 📊 Query & Upload History
All user actions (queries + uploads) are saved in MongoDB.
You can view:
🕓 Date of submission
🔎 Query text or 📄 filename
✅ Decision or status
📥 Action (View justification or Download file)

### 🧰 Requirements
Python 3.7+
MongoDB (running locally on localhost:27017)

```bash
pip install -r requirements.txt
```
