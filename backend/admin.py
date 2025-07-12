from flask import Blueprint, jsonify

admin_bp = Blueprint("admin", __name__)

@admin_bp.route("/admin/settings", methods=["GET"])
def admin_settings():
    return jsonify({
        "site_name": "Luna Ai",
        "theme": "Dark",
        "logo": "/static/logo.png"
    })
