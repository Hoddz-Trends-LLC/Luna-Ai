from flask import Blueprint, request, jsonify
import requests, os, jwt, sqlite3
from dotenv import load_dotenv

load_dotenv()
chat_bp = Blueprint("chat", __name__)
HF_TOKEN = os.getenv("HF_API_TOKEN")
MODEL_URL = "https://api-inference.huggingface.co/models/gpt2"
SECRET_KEY = "luna_secret_key"

def get_db():
    return sqlite3.connect("database.db")

@chat_bp.route("/generate", methods=["POST"])
def generate():
    # Verify and decode token
    token = request.headers.get("Authorization").split()[1]
    decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    user_email = decoded["email"]

    # Get input message
    input_text = request.json.get("input", "")

    # Call Hugging Face API
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    response = requests.post(MODEL_URL, headers=headers, json={"inputs": input_text})
    reply = response.json()[0]["generated_text"]

    # Store chat in DB
    db = get_db()
    user_row = db.execute("SELECT id FROM users WHERE email = ?", (user_email,)).fetchone()
    user_id = user_row[0] if user_row else None
    db.execute("INSERT INTO chats (user_id, message, response) VALUES (?, ?, ?)",
               (user_id, input_text, reply))
    db.commit()

    return jsonify({"response": reply})
