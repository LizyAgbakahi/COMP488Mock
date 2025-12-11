from flask import Flask, jsonify, request
import os
import logging
import json
import sys
from datetime import datetime

app = Flask(__name__)

# ---------- JSON Logging Setup ----------
class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "level": record.levelname,
            "message": record.getMessage(),
            "logger": record.name,
        }
        # Attach request path if available
        try:
            log_record["path"] = request.path
        except RuntimeError:
            log_record["path"] = None
        return json.dumps(log_record)

handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(JsonFormatter())

# Prevent duplicate logs
app.logger.handlers.clear()
app.logger.setLevel(logging.INFO)
app.logger.addHandler(handler)

# ---------------------------------------------------------------

# Sample order data
ORDERS = [
    {"id": 1, "customer": "Sarah Chen", "total": 1549.98, "status": "shipped", "date": "2025-10-10"},
    {"id": 2, "customer": "Marcus Williams", "total": 99.99, "status": "processing", "date": "2025-10-12"},
    {"id": 3, "customer": "Emily Rodriguez", "total": 449.00, "status": "delivered", "date": "2025-10-08"},
    {"id": 4, "customer": "James Park", "total": 1199.00, "status": "pending", "date": "2025-10-14"}
]

@app.route('/health', methods=['GET'])
def health():
    app.logger.info("Health check for order-api")
    return jsonify({
        "status": "healthy", 
        "service": "order-api"
    }), 200

@app.route('/ready', methods=['GET'])
def ready():
    app.logger.info("Readiness check for order-api")
    return jsonify({
        "status": "ready", 
        "service": "order-api"
    }), 200

@app.route('/', methods=['GET'])
def index():
    app.logger.info("Root endpoint called")
    return jsonify({
        "message": "Order API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "ready": "/ready",
            "orders": "/orders"
        }
    }), 200

@app.route('/orders', methods=['GET'])
def get_orders():
    app.logger.info("GET /orders - returning all orders")
    return jsonify({"orders": ORDERS}), 200

@app.route('/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    app.logger.info(f"GET /orders/{order_id} called")
    order = next((o for o in ORDERS if o['id'] == order_id), None)

    if order:
        app.logger.info(f"Order {order_id} found")
        return jsonify(order), 200

    app.logger.warning(f"Order {order_id} not found")
    return jsonify({"error": "Order not found"}), 404

# ---------------------------------------------------------------

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5001))
    app.run(host='0.0.0.0', port=port, debug=False)
