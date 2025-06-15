from flask import Blueprint, jsonify
from bson import ObjectId
from routes import db
from LLM import ai_services

ai_route = Blueprint("ai_routes", __name__)

@ai_route.route("/api/ai/suggest_recipe/<product_id>", methods=["GET"])
def suggest_recipe(product_id):
    try:
        product = db.products.find_one({"_id": ObjectId(product_id)})
        if not product:
           return jsonify({"error": "Product not found"}), 404

        response = ai_services.ask_ai_for_recipe(product["name"])
        return jsonify({"recipe": response})
    except Exception as ex:
        return jsonify({"error": str(ex)}), 500 