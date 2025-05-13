from flask import request
from smartCartApp.utils.jwt_utils import decode_token

class Auth:
    @staticmethod
    def get_current_user_id():
            auth_headers = request.headers.get("Authorization")
            if not auth_headers:
                return None
            
            token = auth_headers.split(" ")[1]
            load = decode_token(token)
            if load:
                return load["user_id"]
            return None