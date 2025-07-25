from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
CORS(app)

# MongoDB setup
client = MongoClient("mongodb://localhost:27017/")
db = client["user_db"]
users_collection = db["users"]

# Base path (same directory as app.py)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Routes to serve HTML files
@app.route("/")
def home():
    return send_file(os.path.join(BASE_DIR, "login.html"))


@app.route("/index.html")
def index():
    return send_file(os.path.join(BASE_DIR, "index.html"))

@app.route("/submit-query.html")
def submit_query():
    return send_file(os.path.join(BASE_DIR, "submit-query.html"))

@app.route("/upload-documents.html")
def upload_documents():
    return send_file(os.path.join(BASE_DIR, "upload-documents.html"))

@app.route("/view-history.html")
def view_history():
    return send_file(os.path.join(BASE_DIR, "view-history.html"))

@app.route("/login.html")
def login_page():
    return send_file(os.path.join(BASE_DIR, "login.html"))


# Signup API
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

# Login API
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

if __name__ == "__main__":
    app.run(debug=True)
