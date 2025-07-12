from flask import Blueprint, request, jsonify
import requests, os, jwt
from dotenv import load_dotenv

load_dotenv()
chat_bp = Blueprint("chat", __name__)
HF_TOKEN = os.getenv("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")
MODEL_URL = "https://api-inference.huggingface.co/models/gpt2"

@chat_bp.route("/generate", methods=["POST"])
def generate():
    token = request.headers.get("Authorization").split()[1]
    jwt.decode(token, "luna_secret_key", algorithms=["HS256"])

    input_text = request.json.get("input", "")
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    response = requests.post(MODEL_URL, headers=headers, json={"inputs": input_text})
    return jsonify(response.json())
