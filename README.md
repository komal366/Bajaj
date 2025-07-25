# 🧠 Policy & Claim Query Analyzer

A smart web app to analyze insurance queries using natural language and document understanding.

---

## 🚀 Features

1. **🔐 Login/Signup**  
   - User roles: Admin, Agent, Normal User  
   - Redirects to dashboard after login

2. **🏠 Dashboard**  
   - Quick links: Submit Query, Upload Documents, View History

3. **💬 Submit Query**  
   - Enter query (e.g., "46M, recent surgery, ₹15,000 claim")  
   - Optionally upload policy/hospital docs

4. **📄 Upload Documents**  
   - Upload `.pdf`, `.docx`, or `.eml`  
   - Extracted text stored in vector DB (FAISS/Pinecone)

5. **🔍 Query Processing**  
   - LLM parses query, matches clauses, makes decision  
   - Approves/Rejects with explanation and matched clauses

6. **✅ Result Page**  
   - Shows decision, amount, justification  
   - Option to export PDF/JSON

7. **🕓 History Page**  
   - Lists all past queries with results

8. **⚙️ Admin Panel** *(Admin only)*  
   - Manage users, view logs, reprocess queries

---

## 🛠️ Tech Stack
- Frontend: HTML, TailwindCSS  
- Backend: Flask / Node.js  
- DB: MongoDB / Firebase  
- AI: GPT / LLMs  
- Vector DB: FAISS / Pinecone  

---

## 📦 Setup

```bash
git clone https://github.com/your-repo.git
cd your-repo
pip install -r requirements.txt
python app.py
