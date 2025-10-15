from flask import Flask, jsonify
import os

app = Flask(__name__)

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
    return jsonify({
        "status": "healthy", 
        "service": "product-api"
    }), 200

@app.route('/ready', methods=['GET'])
def ready():
    """Readiness probe endpoint"""
    return jsonify({
        "status": "ready", 
        "service": "product-api"
    }), 200

@app.route('/', methods=['GET'])
def index():
    """Root endpoint"""
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
    return jsonify({"products": PRODUCTS}), 200

@app.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    """Get specific product by ID"""
    product = next((p for p in PRODUCTS if p['id'] == product_id), None)
    if product:
        return jsonify(product), 200
    return jsonify({"error": "Product not found"}), 404

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)