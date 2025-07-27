SmartQuery AI - Insurance Query Assistant
SmartQuery AI is an intelligent web application that helps users understand their insurance policy coverage by asking natural language queries. The system extracts relevant clauses from insurance documents using a semantic similarity model and provides structured answers including decision, claim amount, justification, and matched clauses.

Features
AI-powered semantic search over insurance documents

Submit queries related to policies via text

Optional document upload for query-specific analysis

Real-time decision support (Approved/Rejected)

Claim justification with matched policy clauses

Secure user authentication (Sign up / Login)

Dashboard with personalized greeting and query submission

View complete query history

Responsive UI with Tailwind CSS

Technologies Used
Frontend
HTML, TailwindCSS, JavaScript

Lucide Icons (Optional)

Responsive design for mobile and desktop

Backend
Python (Flask)

PyMuPDF for PDF parsing

SentenceTransformer with paraphrase-MiniLM-L6-v2 model

MongoDB (via PyMongo)

JWT/localStorage for user session (basic)

AI/ML
Sentence-BERT for semantic similarity

Clause extraction using regex and section title patterns

How It Works
User submits a query (optionally uploading a policy PDF).

The system extracts clauses from the uploaded document or from a predefined dataset.

The query is semantically compared to the clauses using Sentence-BERT.

The system identifies top relevant clauses and provides:

Approval decision

Claim amount

Justification (based on clause content and score)

Matched clause(s)

The query is stored and displayed in the user’s history.

Setup
git clone https://github.com/your-repo.git
pip install -r requirements.txt
python app.py
