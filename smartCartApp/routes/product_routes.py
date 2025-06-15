from flask import Blueprint, request, jsonify
from repositories.repository_product import RepositoryProducts
from routes import db


product_routes = Blueprint('product_routes', __name__)

# Get all products
@product_routes.route("/products", methods=["GET"])
def get_products():
    products = RepositoryProducts().get_all_products()
    for prod in products:
        prod["_id"] = str(prod["_id"])
    return jsonify(products), 200

# Get a product by id
@product_routes.route("/products/<product_id>", methods=["GET"])
def get_product_by_id(product_id):
    product = RepositoryProducts().get_by_id(product_id)
    if not product:
        return jsonify({"error": "Product not found"}), 404
    product["_id"] = str(product["_id"])
    return jsonify(product), 200

# Create a new product
@product_routes.route("/products", methods= ["POST"])
def create_product():
    product_data = request.get_json()
    try:
        inserted_id = RepositoryProducts().insert_product(product_data)
        return jsonify({"message": "Product inserted", "id": str(inserted_id)}), 201
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception as ex:
        return jsonify({"error": "Internal server error"}), 500

# Update an existing product
@product_routes.route("/products/<product_id>", methods=["PUT"])
def update_product(product_id):
    updates = request.get_json()
    result = RepositoryProducts().update(product_id, updates)
    if result.matched_count == 0:
        return jsonify({"error": "Product not exist"}), 400
    return jsonify({"message": "Product updated"}), 200

# Delete product
@product_routes.route("/products/<product_id>", methods=["DELETE"])
def delete_product(product_id):
    result = RepositoryProducts().delete(product_id)
    if result.deleted_count == 0:
        return jsonify({"error": "Product not found"}),404
    return jsonify({"message": "Product deleted"}), 200

#Delete all products
@product_routes.route("/products", methods=["DELETE"])
def delete_all_products():
    result = RepositoryProducts.delete_all()
    return jsonify({"message": f"{result.deleted_count} products deleted"}), 200