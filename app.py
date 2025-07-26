from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
import os
import datetime
import fitz  # PyMuPDF
import json
import re
import google.generativeai as genai

# ✅ Configure Gemini API Key
genai.configure(api_key="your key")  # Replace this with your key

app = Flask(__name__)
CORS(app)

# ✅ MongoDB setup
client_mongo = MongoClient("mongodb://localhost:27017/")
db = client_mongo["user_db"]
users_collection = db["users"]
queries_collection = db["queries"]

# ✅ Dataset folder path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_FOLDER = os.path.join(BASE_DIR, "dataset")
dataset_text = ""

# ✅ Load dataset
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

# ✅ Auth
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

# ✅ Submit Query
@app.route("/submit-query", methods=["POST"])
def handle_query():
    data = request.json
    name = data.get("name")
    query = data.get("query")

    prompt = f"""
You are an insurance assistant AI. Use the following policy document to evaluate the user's query.

--- Policy Document Start ---
{dataset_text[:10000]}
--- Policy Document End ---

User Query:
"{query}"

Respond in ONLY valid JSON in this format:

{{
  "decision": "Approved/Rejected/Partially Approved",
  "amount": "₹amount or 'N/A'",
  "justification": "Explain clearly using relevant clauses",
  "matched_clauses": [
    "Section 2.1: ...",
    "Section 4.3: ..."
  ]
}}
"""

    try:
        # ✅ Gemini LLM Call
        model = genai.GenerativeModel("gemini-pro")
        chat = model.start_chat()
        response = chat.send_message(prompt)
        content = response.text

        print("🔍 Gemini Response:\n", content)

        # ✅ Extract JSON
        match = re.search(r"\{.*\}", content, re.DOTALL)
        if not match:
            raise ValueError("No valid JSON found")

        result = json.loads(match.group(0))

        # ✅ Save to DB
        queries_collection.insert_one({
            "name": name,
            "query": query,
            "decision": result.get("decision", "Unknown"),
            "amount": result.get("amount", "N/A"),
            "justification": result.get("justification", ""),
            "matched_clauses": result.get("matched_clauses", []),
            "date": datetime.datetime.now()
        })

        return jsonify(result)

    except Exception as e:
        print("❌ Gemini Error:", e)
        return jsonify({
            "decision": "Unknown",
            "amount": "N/A",
            "justification": "An error occurred while processing your query.",
            "matched_clauses": []
        }), 500

# ✅ Query History
@app.route("/query-history", methods=["GET"])
def get_history():
    queries = list(queries_collection.find({}, {"_id": 0}))
    return jsonify({"queries": queries})

# ✅ Run App
if __name__ == "__main__":
    app.run(debug=True)
