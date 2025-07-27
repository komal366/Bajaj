from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
import os
import datetime
import fitz  # PyMuPDF
import json
import re
from sentence_transformers import SentenceTransformer, util
import torch

app = Flask(__name__)
CORS(app)

# ✅ MongoDB setup
client_mongo = MongoClient("mongodb://localhost:27017/")
db = client_mongo["user_db"]
users_collection = db["users"]
queries_collection = db["queries"]

# ✅ Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_FOLDER = os.path.join(BASE_DIR, "dataset")

# ✅ Load dataset text
def load_dataset_text():
    combined = ""
    for filename in os.listdir(DATASET_FOLDER):
        if filename.endswith(".pdf"):
            path = os.path.join(DATASET_FOLDER, filename)
            try:
                with fitz.open(path) as doc:
                    for page in doc:
                        combined += page.get_text()
            except Exception as e:
                print(f"❌ Failed to load {filename}: {e}")
    return combined

dataset_text = load_dataset_text()

def extract_clauses(text):
    # Split on common section titles or headings
    pattern = re.compile(r'((?:[A-Z][a-z]+ )?(?:Cover|Covers|We will not cover|We will cover|expenses|Add On Wordings)[^\n]*)\n+(.*?)(?=\n[A-Z].*?Cover|\nWe will not cover|\nAdd On Wordings|$)', re.DOTALL)
    matches = pattern.findall(text)

    clauses = []
    for title, body in matches:
        cleaned_title = title.strip().replace('\n', ' ')
        cleaned_body = body.strip().replace('\n', ' ')
        clause = f"{cleaned_title}: {cleaned_body}"
        clauses.append(clause)

    print(f"✅ Extracted {len(clauses)} full clauses.")
    return clauses


policy_clauses = extract_clauses(dataset_text)

# ✅ Load model
model = SentenceTransformer("paraphrase-MiniLM-L6-v2")

# ✅ ROUTES
@app.route("/")
def home():
    return send_file(os.path.join(BASE_DIR, "login.html"))

@app.route("/submit-query.html")
def submit_query_page():
    return send_file(os.path.join(BASE_DIR, "submit-query.html"))

@app.route("/index.html")
def index():
    return send_file(os.path.join(BASE_DIR, "index.html"))

@app.route("/view-history.html")
def view_history():
    return send_file(os.path.join(BASE_DIR, "view-history.html"))

@app.route("/login.html")
def login_page():
    return send_file(os.path.join(BASE_DIR, "login.html"))

# ✅ AUTH
@app.route("/signup", methods=["POST"])
def signup():
    data = request.json
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    if users_collection.find_one({"email": email}):
        return jsonify({"message": "User already exists"}), 400

    hashed_pw = generate_password_hash(password)
    users_collection.insert_one({
        "name": name,
        "email": email,
        "password": hashed_pw
    })

    return jsonify({"message": "Signup successful"}), 200

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    user = users_collection.find_one({"email": email})
    if user and check_password_hash(user["password"], password):
        return jsonify({
            "message": "Login successful",
            "user": {
                "name": user["name"],
                "email": user["email"]
            }
        }), 200

    return jsonify({"message": "Invalid email or password"}), 401

# ✅ SUBMIT QUERY
@app.route("/submit-query", methods=["POST"])
def handle_query():
    data = request.json
    name = data.get("name")
    query = data.get("query")

    try:
        if not policy_clauses:
            raise ValueError("No policy clauses available.")

        # Embeddings
        query_embedding = model.encode(query, convert_to_tensor=True)
        clause_embeddings = model.encode(policy_clauses, convert_to_tensor=True)

        # Similarity calculation
        similarities = util.pytorch_cos_sim(query_embedding, clause_embeddings)[0]
        top_k = 3
        top_indices = torch.topk(similarities, k=top_k).indices

        # Extract top matched clauses and remove duplicates
        seen = set()
        matched_clauses = []
        for i in top_indices:
            clause = policy_clauses[i]
            cleaned = clause.strip()
            if cleaned not in seen:
                seen.add(cleaned)
                matched_clauses.append(cleaned)
        matched_clauses = matched_clauses[:top_k]

        # Decision logic
        max_sim = float(similarities[top_indices[0]])
        decision = "Approved" if max_sim > 0.5 else "Rejected"
        amount = "₹25,000" if decision == "Approved" else "N/A"

        # Extract first clause snippet for justification
        first_clause_summary = matched_clauses[0][:100].strip().replace('\n', ' ')
        justification = f"Covered under clause: \"{first_clause_summary}...\" (similarity: {max_sim:.2f})"

        # Save to DB
        queries_collection.insert_one({
            "name": name,
            "query": query,
            "decision": decision,
            "amount": amount,
            "justification": justification,
            "matched_clauses": matched_clauses,
            "date": datetime.datetime.now()
        })

        return jsonify({
            "decision": decision,
            "amount": amount,
            "justification": justification,
            "matched_clauses": matched_clauses
        })

    except Exception as e:
        print("❌ Model Error:", e)
        return jsonify({
            "decision": "Unknown",
            "amount": "N/A",
            "justification": "An error occurred while processing your query.",
            "matched_clauses": []
        }), 500


# ✅ QUERY HISTORY
@app.route("/query-history", methods=["GET"])
def get_history():
    queries = list(queries_collection.find({}, {"_id": 0}))
    return jsonify({"queries": queries})

# ✅ Run app
if __name__ == "__main__":
    app.run(debug=True)
