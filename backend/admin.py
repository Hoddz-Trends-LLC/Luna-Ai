from flask import Blueprint, request, jsonify
import sqlite3
import jwt

def is_authorized_admin(request):
    token = request.headers.get("Authorization")
    if not token:
        return False
    try:
        decoded = jwt.decode(token.split()[1], "luna_secret_key", algorithms=["HS256"])
        email = decoded["email"]
        db = get_db()
        row = db.execute("SELECT is_admin FROM users WHERE email = ?", (email,)).fetchone()
        return row and row[0] == 1
    except Exception:
        return False

@admin_bp.route("/admin/users", methods=["GET"])
def list_users():
    if not is_authorized_admin(request):
        return jsonify({"error": "Access denied"}), 403

    db = get_db()
    users = db.execute("SELECT id, name, email, created_at FROM users").fetchall()
    return jsonify([dict(zip(["id", "name", "email", "created_at"], row)) for row in users])


admin_bp = Blueprint("admin", __name__)
DATABASE = "database.db"

def get_db():
    return sqlite3.connect(DATABASE)

@admin_bp.route("/admin/users", methods=["GET"])
def list_users():
    db = get_db()
    users = db.execute("SELECT id, name, email, created_at FROM users").fetchall()
    return jsonify([dict(zip(["id", "name", "email", "created_at"], row)) for row in users])

@admin_bp.route("/admin/delete_user/<int:user_id>", methods=["POST"])
def delete_user(user_id):
    db = get_db()
    db.execute("DELETE FROM users WHERE id = ?", (user_id,))
    db.commit()
    return jsonify({"msg": f"User {user_id} deleted"})

@admin_bp.route("/admin/settings", methods=["GET", "POST"])
def site_settings():
    if request.method == "GET":
        db = get_db()
        row = db.execute("SELECT site_name, theme, logo FROM settings LIMIT 1").fetchone()
        return jsonify(dict(zip(["site_name", "theme", "logo"], row)) if row else {})
    
    data = request.json
    db = get_db()
    db.execute("UPDATE settings SET site_name = ?, theme = ?, logo = ?",
               (data["site_name"], data["theme"], data["logo"]))
    db.commit()
    return jsonify({"msg": "Settings updated"})
