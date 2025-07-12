from flask import Flask
from auth import auth_bp
from chat import chat_bp
from admin import admin_bp

app = Flask(__name__)
app.secret_key = "luna_secret_key"

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(chat_bp)
app.register_blueprint(admin_bp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
