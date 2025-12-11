from flask import Flask, jsonify, request
import os
import logging
import json
import sys

app = Flask(__name__)

# ---------- JSON Logging Setup ----------

class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "level": record.levelname,
            "message": record.getMessage(),
            "logger": record.name,
        }
        # Attach request path if we are in a request context
        try:
            log_record["path"] = request.path
        except RuntimeError:
            log_record["path"] = None
        return json.dumps(log_record)

handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(JsonFormatter())

# Avoid duplicate handlers
app.logger.handlers.clear()
app.logger.setLevel(logging.INFO)
app.logger.addHandler(handler)

# ---------- App Logic ----------

# Sample product data
PRODUCTS = [
    {"id": 1, "name": "Dell XPS 15 Laptop", "price": 1299.99, "stock": 23},
    {"id": 2, "name": "Logitech MX Master 3", "price": 99.99, "stock": 147},
    {"id": 3, "name": "Mechanical Keyboard - Cherry MX Blue", "price": 129.50, "stock": 64},
    {"id": 4, "name": "LG UltraWide 34\" Monitor", "price": 449.99, "stock": 31},
    {"id": 5, "name": "Sony WH-1000XM5 Headphones", "price": 379.99, "stock": 89}
]

@app.route('/health', methods=['GET'])
def health():
    """Liveness probe endpoint"""
    app.logger.info("Health check for product-api")
    return jsonify({
        "status": "healthy",
        "service": "product-api"
    }), 200

@app.route('/ready', methods=['GET'])
def ready():
    """Readiness probe endpoint"""
    app.logger.info("Readiness check for product-api")
    return jsonify({
        "status": "ready",
        "service": "product-api"
    }), 200

@app.route('/', methods=['GET'])
def index():
    """Root endpoint"""
    app.logger.info("Root endpoint called for product-api")
    return jsonify({
        "message": "Product API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "ready": "/ready",
            "products": "/products"
        }
    }), 200

@app.route('/products', methods=['GET'])
def get_products():
    """Get all products"""
    app.logger.info("GET /products - returning %d products", len(PRODUCTS))
    return jsonify({"products": PRODUCTS}), 200

@app.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    """Get specific product by ID"""
    app.logger.info("GET /products/%d", product_id)
    product = next((p for p in PRODUCTS if p['id'] == product_id), None)
    if product:
        app.logger.info("Product %d found", product_id)
        return jsonify(product), 200
    app.logger.warning("Product %d not found", product_id)
    return jsonify({"error": "Product not found"}), 404

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.logger.info("Starting product-api on port %d", port)
    app.run(host='0.0.0.0', port=port, debug=False)
