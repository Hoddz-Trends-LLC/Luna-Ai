from flask import Blueprint, request, jsonify
import sqlite3
import jwt, datetime
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint("auth", __name__)
SECRET_KEY = "luna_secret_key"

def get_db():
    return sqlite3.connect("database.db")

@auth_bp.route("/signup", methods=["POST"])
def signup():
    data = request.json
    hashed = generate_password_hash(data["password"])
    db = get_db()
    db.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
               (data["name"], data["email"], hashed))
    db.commit()
    return jsonify({"msg": "Account created successfully"})

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    db = get_db()
    user = db.execute("SELECT * FROM users WHERE email = ?", (data["email"],)).fetchone()
    if user and check_password_hash(user[3], data["password"]):
        token = jwt.encode({"email": user[2], "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24)},
                           SECRET_KEY, algorithm="HS256")
        return jsonify({"token": token})
    return jsonify({"error": "Invalid credentials"}), 401
