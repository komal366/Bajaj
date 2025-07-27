SmartQuery AI
SmartQuery AI is an intelligent insurance query assistant that uses machine learning and natural language processing (NLP) to analyze insurance-related queries. It semantically searches uploaded policy documents or a predefined dataset and provides structured responses with decisions, justification, and matched policy clauses.

Features
User authentication (Sign Up / Login)

Submit queries with or without uploading a document

Real-time semantic matching using Sentence Transformers (DistilBERT)

Outputs:

Approval/Reject decision

Estimated claim amount

Matched policy clauses

Justification

Query and document history view

Responsive, modern UI built with TailwindCSS

Setup
bash
Copy
Edit
git clone https://github.com/your-repo.git
cd your-repo
pip install -r requirements.txt
python app.py
Visit: http://localhost:5000

Folder Structure
php
Copy
Edit
your-repo/
├── app.py                    # Main Flask backend
├── dataset/                  # Contains default insurance policy PDFs
├── static/                   # (Optional) CSS/JS files if extracted
├── templates/ or HTML files  # login.html, submit-query.html, etc.
├── uploads/                  # Stores uploaded policy documents
├── requirements.txt
Tech Stack
Frontend:

HTML, TailwindCSS

Lucide Icons (optional)

Vanilla JavaScript

Backend:

Python Flask

MongoDB (via PyMongo)

PyMuPDF (fitz) for PDF parsing

SentenceTransformer (paraphrase-MiniLM-L6-v2) for semantic matching

How It Works
User submits a query and (optionally) uploads a PDF policy document.

The system extracts clauses from the document (or falls back to the dataset).

It performs semantic search using SentenceTransformer.

Returns a structured response with:

Decision (Approved/Rejected)

Estimated claim amount

Justification

Matched policy clauses

Policy name (if provided)

History Page
All submitted queries and uploaded documents are stored in MongoDB.

The "View History" page shows:

Query date

Query text or uploaded file name

Decision or upload status

Option to view justification or download document

Requirements
Python 3.7+

MongoDB running locally on mongodb://localhost:27017

Install dependencies:

bash
Copy
Edit
pip install -r requirements.txt
