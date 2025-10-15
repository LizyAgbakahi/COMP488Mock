from flask import Flask, jsonify
import os
from datetime import datetime

app = Flask(__name__)

# Sample order data
ORDERS = [
    {"id": 1, "customer": "Sarah Chen", "total": 1549.98, "status": "shipped", "date": "2025-10-10"},
    {"id": 2, "customer": "Marcus Williams", "total": 99.99, "status": "processing", "date": "2025-10-12"},
    {"id": 3, "customer": "Emily Rodriguez", "total": 449.00, "status": "delivered", "date": "2025-10-08"},
    {"id": 4, "customer": "James Park", "total": 1199.00, "status": "pending", "date": "2025-10-14"}
]

@app.route('/health', methods=['GET'])
def health():
    """Liveness probe endpoint"""
    return jsonify({
        "status": "healthy", 
        "service": "order-api"
    }), 200

@app.route('/ready', methods=['GET'])
def ready():
    """Readiness probe endpoint"""
    return jsonify({
        "status": "ready", 
        "service": "order-api"
    }), 200

@app.route('/', methods=['GET'])
def index():
    """Root endpoint"""
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
    """Get all orders"""
    return jsonify({"orders": ORDERS}), 200

@app.route('/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    """Get specific order by ID"""
    order = next((o for o in ORDERS if o['id'] == order_id), None)
    if order:
        return jsonify(order), 200
    return jsonify({"error": "Order not found"}), 404

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5001))
    app.run(host='0.0.0.0', port=port, debug=False)