from flask import Flask
import os

app = Flask(__name__)

VERSION = os.getenv("APP_VERSION", "1.0.0")
ENVIRONMENT = os.getenv("ENVIRONMENT", "dev")


@app.route("/")
def home():
    return {
        "service": "frontend",
        "version": VERSION,
        "environment": ENVIRONMENT,
        "message": "Welcome to the Dev-to-Prod Promotion Demo"
    }


@app.route("/health")
def health():
    return {
        "status": "healthy"
    }


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
