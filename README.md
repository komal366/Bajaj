🤖 SmartQuery AI
SmartQuery AI is an AI-powered insurance query assistant that uses NLP + ML to intelligently analyze user questions, extract relevant information from insurance policy documents, and provide structured answers like claim approval, justification, and matched policy clauses.

🚀 Features
🔐 User Authentication (Sign Up / Login)

📤 Submit Queries with or without PDF document

🤖 AI-Based Semantic Search using Sentence Transformers

✅ Real-time Decisions: Approved / Rejected

💰 Claim Amount Estimation

📚 Matched Policy Clauses + Justification

📜 Policy Name Detection

📂 Query & Document History with Download/View

📦 Setup
bash```
git clone https://github.com/your-repo.git
cd your-repo
pip install -r requirements.txt
python app.py
🔗 Open in browser: http://localhost:5000

🗂️ Folder Structure
graphql
Copy
Edit
SmartQuery-AI/
├── app.py                    # 🔁 Main Flask backend
├── dataset/                  # 📄 Predefined PDF policies
├── uploads/                  # ⬆️ Uploaded documents
├── requirements.txt          # 🧪 Python dependencies
├── login.html                # 🔐 Auth UI
├── submit-query.html         # 🧾 Query form UI
├── view-history.html         # 🕓 Query/document history UI
└── index.html                # 🏠 Dashboard
⚙️ Tech Stack
🖥️ Frontend
HTML, TailwindCSS

Lucide Icons

Vanilla JavaScript

🧠 Backend
Python + Flask

MongoDB (PyMongo)

PyMuPDF (fitz) for PDF parsing

Sentence Transformers (MiniLM / DistilBERT)

🧪 How It Works
User submits a query and (optionally) uploads a PDF.

System extracts clauses using regex + PDF parser.

Encodes both query and clauses using Sentence-BERT.

Calculates semantic similarity and selects top matches.

Returns:

✅ Decision (Approved/Rejected)

💵 Estimated Amount

🧾 Justification

📌 Matched Clauses

📄 Policy Name (if provided)

📊 View History
All queries & uploads saved in MongoDB.

UI table shows:

📅 Date

💬 Query or 📄 Uploaded File

⚙️ Status (Approved / Rejected / Uploaded)

🔍 View/Download Options

🧰 Requirements
Python 3.7+

MongoDB (local) on mongodb://localhost:27017

bash
Copy
Edit
pip install -r requirements.txt
