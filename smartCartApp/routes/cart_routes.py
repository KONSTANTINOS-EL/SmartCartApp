from bson import ObjectId
from flask import Blueprint, request, jsonify
from repositories.repository_product import RepositoryProducts
from repositories.repository_cart import RepositoryCart
from routes.extract_user_id.extract import Auth
from exceptions.smartCart_exceptions import CartNotFound, InvalidProductExcepton, DatabaseException
from routes import db


product_routes = Blueprint('product_routes', __name__)
cart_routes = Blueprint('cart_routes', __name__)


#----------------PRODUCTS-----------------#

# Get all products
# @product_routes.route("/products", methods=["GET"])
# def get_products():
#     products = RepositoryProducts.get_all_products()
#     for prod in products:
#         prod["_id"] = str(prod["_id"])
#     return jsonify(products), 200

# # Get a product by id
# @product_routes.route("/products/<product_id>", methods=["GET"])
# def get_product_by_id(product_id):
#     product = RepositoryProducts.get_by_id(product_id)
#     if not product:
#         return jsonify({"error": "Product not found"}), 404
#     product["_id"] = str(product["_id"])
#     return jsonify(product), 200

# # Create a new product
# @product_routes.route("/products", methods= ["POST"])
# def create_product():
#     product_data = request.get_json()
#     try:
#         inserted_id = RepositoryProducts.insert_product(product_data)
#         return jsonify({"message": "Product inserted", "id": str(inserted_id)}), 201
#     except ValueError as ve:
#         return jsonify({"error": str(ve)}), 400
#     except Exception as ex:
#         return jsonify({"error": "Internal server error"}), 500

# # Update an existing product
# @product_routes.route("/products/<product_id>", methods=["PUT"])
# def update_product(product_id):
#     updates = request.get_json()
#     result = RepositoryProducts.update(product_id, updates)
#     if result.matched_count == 0:
#         return jsonify({"error": "Product not exist"}), 400
#     return jsonify({"message": "Product updated"}), 200

# # Delete product
# @product_routes.route("/products/<product_id>", methods=["DELETE"])
# def delete_product(product_id):
#     result = RepositoryProducts.delete(product_id)
#     if result.deleted_count == 0:
#         return jsonify({"error": "Product not found"}),404
#     return jsonify({"message": "Product deleted"}), 200

# #Delete all products
# @product_routes.route("/products", methods=["DELETE"])
# def delete_all_products():
#     result = RepositoryProducts.delete_all()
#     return jsonify({"message": f"{result.deleted_count} products deleted"}), 200

#----------------CART-----------------#

#Create cart
@cart_routes.route("/carts/create", methods=["POST"])
def create_cart():
    try:
        user_id = request.json["user_id"]
        repo_cart = RepositoryCart()
        cart_id = repo_cart.create_cart(user_id)
        return jsonify({"message": "Cart created", "cart_id": cart_id}), 201
    except Exception as ex:
        return jsonify({"error": str(ex)}), 500
    
#Get cart
@cart_routes.route("/carts/get_cart", methods=["POST"])
def get_cart():
    try:
        
        current_user_id = Auth.get_current_user_id()

        if not current_user_id:
            return jsonify({"error": "Unauthorized"}), 401
        
        repo_cart = RepositoryCart(db)
        cart = repo_cart.get_cart(current_user_id)
        if not cart:
            return jsonify({"error": "Cart is Empty"}), 200

        cart["_id"] = str(cart["_id"])
        cart["user_id"] = str(cart["user_id"])
        for product in cart.get('products', []):
            product["product_id"] = str(product["product_id"]) 
            product["name"]
            
 
        return jsonify(cart), 200
    except CartNotFound as ex:
        return jsonify({"error": str(ex)}), 404
    except Exception as ex:
        return jsonify({"error": str(ex)}), 500
   

@cart_routes.route("/carts/add_product", methods=["POST"])
def add_to_cart():
    try:
        data = request.get_json()
        current_user_id = Auth.get_current_user_id()

        if not current_user_id:
            return jsonify({"error": "Unauthorized"}), 401
        
        product_id = data.get("product_id")
        quantity = data.get("quantiry", 1)

        try:
            result = RepositoryCart(db).add_product(current_user_id, product_id, quantity)
            return jsonify({"message": result}), 200
        except Exception as ex:
            return jsonify({"error": str(ex)}), 400
        
    except CartNotFound as ex:
        return jsonify({"error": str(ex)}), 404
    except InvalidProductExcepton as ex:
        return jsonify({"error": str(ex)}), 400
    except DatabaseException as ex:
        return jsonify({"error": str(ex)}), 500
    except Exception as ex:
        return jsonify({"error": str(ex)}), 500


# Remove Product 
@cart_routes.route("/cart/remove_product", methods=["POST"])
def remove_product():
    try:
        req = request.json
        user_id = req["user_id"]
        product_id = req["product_id"]
        repo_cart = RepositoryCart(db)

        repo_cart.remove_product(user_id, product_id)
        return ({"message": "Product removed from cart"}), 200
    except Exception as ex:
        return jsonify({"error": str(ex)}), 500
    
#Update quantity in cart
@cart_routes.route("/carts/update_quantity", methods=["POST"])
def update_quantity():
    try:
        req = request.json
        user_id = req["user_id"]
        product_id = req["product_id"]
        new_quantity = req["quantity"]
        repo_cart = RepositoryCart()
        repo_cart.update_quantity(user_id, product_id,new_quantity)
        
        return jsonify({"message": "Product quantiry updated"}), 200
    except Exception as ex:
        return jsonify({"error": str(ex)}), 500

#Clear cart
@cart_routes.route("/carts/clear", methods=["POST"])
def clear_cart():
    try:
        user_id = Auth.get_current_user_id()
        repo_cart = RepositoryCart(db)
        repo_cart.clear_cart(user_id)

        return jsonify({"message": "Car is cleared"}), 200
    except Exception as ex:
        return jsonify({"error": str(ex)})
    
#Delete cart
@cart_routes.route("/carts/delete_all_carts", methods=["POST"])
def delete_all_carts():
    try:
        user_id = Auth.get_current_user_id()
        repo_cart = RepositoryCart(db)
        repo_cart.delete_all_carts(user_id)

        return jsonify({"message": "Cart is deleted"}), 200
    except Exception as ex:
        return jsonify({"error": str(ex)}), 500
    
@cart_routes.route("/cart/delete_product_from_cart/<product_id>", methods=["DELETE"])
def delete_product(product_id):
    try:
        user_id = Auth.get_current_user_id()
        repo_cart = RepositoryCart(db)
        repo_cart.delet_product_from_cart(user_id, product_id)

        return jsonify({"message": "Product from cart is deleted"}), 200
    except Exception as ex:
        return jsonify({"error": str(ex)})