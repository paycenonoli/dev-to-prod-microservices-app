from flask import Flask
import os
import requests

app = Flask(__name__)

VERSION = os.getenv("APP_VERSION", "1.0.0")
ENVIRONMENT = os.getenv("ENVIRONMENT", "dev")

PRODUCT_SERVICE_URL = os.getenv(
    "PRODUCT_SERVICE_URL",
    "http://product-service:8081"
)

ORDER_SERVICE_URL = os.getenv(
    "ORDER_SERVICE_URL",
    "http://order-service:8082"
)


@app.route("/")
def home():
    return {
        "service": "frontend",
        "version": VERSION,
        "environment": ENVIRONMENT,
        "message": "Welcome to the Dev-to-Prod Promotion Demo"
    }


@app.route("/products")
def products():
    response = requests.get(
        f"{PRODUCT_SERVICE_URL}/",
        timeout=5
    )

    return response.json(), response.status_code


@app.route("/orders")
def orders():
    response = requests.get(
        f"{ORDER_SERVICE_URL}/orders",
        timeout=5
    )

    return response.json(), response.status_code


@app.route("/health")
def health():
    return {
        "status": "healthy"
    }


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
