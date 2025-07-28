from backend.auth import auth_bp
from backend.chat import chat_bp
from backend.admin import admin_bp
from flask import Flask

app = Flask(__name__)
app.secret_key = "luna_secret_key"

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(chat_bp)
app.register_blueprint(admin_bp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()

@app.get("/")
def read_root():
    return JSONResponse(content={"message": "Luna AI backend is running"})
