from flask import Flask
import os

app = Flask(__name__)

VERSION = os.getenv("APP_VERSION", "1.0.0")
ENVIRONMENT = os.getenv("ENVIRONMENT", "dev")


ORDERS = [
    {"id": 1001, "product": "Laptop", "status": "shipped"},
    {"id": 1002, "product": "Keyboard", "status": "processing"},
    {"id": 1003, "product": "Mouse", "status": "delivered"}
]


@app.route("/")
def home():
    return {
        "service": "order-service",
        "version": VERSION,
        "environment": ENVIRONMENT,
        "message": "Order Service is running"
    }


@app.route("/orders")
def orders():
    return {
        "service": "order-service",
        "orders": ORDERS
    }


@app.route("/health")
def health():
    return {
        "status": "healthy"
    }


@app.route("/version")
def version():
    return {
        "service": "order-service",
        "version": VERSION,
        "environment": ENVIRONMENT
    }


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8082)
