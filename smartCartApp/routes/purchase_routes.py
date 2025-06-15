from repositories.repository_purchase import RepositoryPurchase
from flask import Blueprint, request, jsonify
from routes.extract_user_id.extract import Auth
from routes import db

purchase_routes = Blueprint('purchase_route', __name__)

@purchase_routes.route("/purchase", methods=["POST"])
def purchase():
    user_id = Auth.get_current_user_id()
    if not user_id:
        return jsonify({"error": "Unauthorized"})
    
    repo_purchase = RepositoryPurchase(db)
    result, status = repo_purchase.purchase_cart(user_id)
    return jsonify(result), status