from flask import Blueprint, request, jsonify
from bson import ObjectId
from smartCartApp import db
from smartCartApp.repositories.repository_analysis import RepositoryAnalysis
from smartCartApp.routes.extract_user_id.extract import Auth

analysis_routes = Blueprint("analysis_routes", __name__)
repo = RepositoryAnalysis(db)

#User statistics
@analysis_routes.route("/api/analysis/user_purchases/<user_id>", methods=["GET"])
def get_user_stats(user_id):
    try:
        user_id = Auth.get_current_user_id()
        stats = repo.get_user_purchase_stattistics(user_id)
        return jsonify(stats), 200
    except Exception as ex:
        return jsonify({"error": str(ex)}),500
    
#Predict next product.
@analysis_routes.route("/api/analysis/predict_next/<user_id>", methods=["GET"])
def predict_next(user_id):
    try:
        user_id = Auth.get_current_user_id()
        top_products = repo.predict_next_products(user_id)
        return jsonify(top_products), 200
    except Exception as ex:
        return jsonify({"error": str(ex)}), 500

    
#Products frequently bought together
@analysis_routes.route("/api/analysis/frequently-bought-togehter/<product_id>", methods=['GET'])
def get_frequently_bought_together(product_id):
    try:
        products = repo.get_frequently_bought_together(product_id)
        return jsonify(products), 200
    except Exception as ex:
        return jsonify({"error": str(ex)}), 500
