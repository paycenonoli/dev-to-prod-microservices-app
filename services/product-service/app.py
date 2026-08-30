from flask import Flask
import os

app = Flask(__name__)

VERSION = os.getenv("APP_VERSION", "1.0.0")
ENVIRONMENT = os.getenv("ENVIRONMENT", "dev")


@app.route("/")
def home():
    return {
        "service": "product-service",
        "version": VERSION,
        "environment": ENVIRONMENT,
        "products": [
            {"id": 1, "name": "Laptop", "price": 1200},
            {"id": 2, "name": "Keyboard", "price": 80},
            {"id": 3, "name": "Mouse", "price": 40}
        ]
    }


@app.route("/health")
def health():
    return {
        "status": "healthy"
    }


@app.route("/version")
def version():
    return {
        "service": "product-service",
        "version": VERSION,
        "environment": ENVIRONMENT
    }


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8081)
