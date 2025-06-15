from flask import Blueprint, request, jsonify
from model.users import User
from repositories.repository_user import RepositoryUser
from utils.password_utils import hash_password, check_password
from utils.jwt_utils import generate_token, decode_token

user_routes = Blueprint("user_routes", __name__)

@user_routes.route("/users/register", methods=["POST"])
def register():
    try:
        req = request.get_json()
        email = req["email"]
        password = req["password"]
        username = req["username"]

        if RepositoryUser.find_by_email(email):
            return jsonify({"error": "Email already exists"}), 409

        hash_pass = hash_password(password)
        user = User(username, email, hash_pass)
        user_id = RepositoryUser.create_user(user)

        return jsonify({"message": "User created", "user_id": user_id}),201
    
    except Exception as ex:
        return jsonify({"error": str(ex)}),500
    
@user_routes.route("/users/login", methods=["POST"])
def login():
    try:
        req = request.get_json()
        email = req["email"]
        password = req["password"]
        user = RepositoryUser.find_by_email(email)

        if not user:
            return jsonify({"error": "Invalid email or password"}), 401

        if not check_password(password, user["password"]):
            return jsonify({"error": "Invalid email or password"}), 401
        
        user["_id"] = str(user["_id"])
        token = generate_token(user["_id"])
        
        return jsonify({"message": "Login successful", "token": token, "user": user}),200
    
    except Exception as ex:
        return jsonify({"error": str(ex)}), 500
    
@user_routes.route("/users/all", methods=["GET"])
def get_all_users():
    try:
        users = RepositoryUser.get_all_users()
        return jsonify(users), 200
    except Exception as ex:
        return jsonify({"error": str(ex)}),500
    


def get_current_user_id():
        auth_headers = request.headers.get("Authorization")
        if not auth_headers:
            return None
        
        token = auth_headers.split(" ")[1]
        load = decode_token(token)
        if load:
            return load["user_id"]
        return None