from flask import Blueprint ,request, jsonify
from smartCartApp import db
from Scraping.web_scraping import scrape_products_from_sklavenitis, scrape_products_from_masouti





webScraping_product_routes = Blueprint('webScraping_product_routes', __name__)

@webScraping_product_routes.route("/serach-product-sklavenitis", methods=["POST"])
def search_and_add_product_sklavenitis():
    data = request.get_json()
    search_term = data.get("query")

    if not search_term:
        return jsonify({"error_message": "Missing search term"}), 400
    
    product_list = scrape_products_from_sklavenitis(search_term)
    if not product_list:
        return jsonify({"error_message": "No products found"}), 404
    
    inserted_products = []

    for product in product_list:
        existing = db.products.find_one({"name": product["name"]})
        if not existing:
            result = db.products.insert_one(product)
            product["_id"] = str(result.inserted_id)
            inserted_products.append(product)
        else:
            existing["_id"] = str(existing["_id"])
            inserted_products.append(existing)

    #Sanitize before returning
    for product in inserted_products:
        product["_id"] = str(product.get("_id", ""))
            
            
    
    return jsonify({"message": "Products added", "product": inserted_products}), 200


@webScraping_product_routes.route("/serach-product-marketin", methods=["POST"])
def search_and_add_product_masoutis():
    data = request.get_json()
    search_term = data.get("query")

    if not search_term:
        return jsonify({"error_message": "Missing search term"},400)
    
    product_list = scrape_products_from_masouti(search_term)
    if not product_list:
        return jsonify({"error_message": "No products found"}, 404)
    
    inserted_products = []

    for product in product_list:
        existing = db.products.find_one({"name": product["name"]})
        if not existing:
            result = db.products.insert_one(product)
            product["_id"] = str(result.inserted_id)
            inserted_products.append(product)
        else:
            existing["_id"] = str(existing["_id"])
            inserted_products.append(existing)

    #Sanitize before returning
    for product in inserted_products:
        product["_id"] = str(product.get("_id", ""))
            
            
    
    return jsonify({"message": "Products added", "product": inserted_products}), 200


    
    