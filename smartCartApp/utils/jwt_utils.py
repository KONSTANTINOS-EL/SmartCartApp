import jwt
from datetime import datetime, timedelta


SECRET_KEY = "chr051099"

def generate_token(user_id):
    load = {
        "user_id": user_id, 
        "exp": datetime.utcnow() + timedelta(hours=24) #token expires in 24 hours
    }

    token = jwt.encode(load, SECRET_KEY, algorithm="HS256")
    return token

def decode_token(token):
    try:
        load = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return load
    except jwt.ExpiredSignatureError:
        return None #token expired
    except jwt.InvalidAlgorithmError:
        return None #invalid token