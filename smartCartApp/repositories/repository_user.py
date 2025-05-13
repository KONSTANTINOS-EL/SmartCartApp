from bson import ObjectId
from smartCartApp import db


users_collection = db["users"]

class RepositoryUser:

    @staticmethod
    def create_user(user):
        result = users_collection.insert_one(user.to_dict())
        return str(result.inserted_id)
    
    @staticmethod
    def find_by_email(email):
        return users_collection.find_one({"email": email})
    
    @staticmethod
    def find_by_id(user_id):
        return users_collection.find_one({"_id": user_id})
    
    @staticmethod
    def get_all_users():
        users = users_collection.find()
        return [
            {
                "_id": str(user["_id"]),
                "email": user["email"],
                "username": user["username"],
                "created_at": user["created_at"]
            }

            for user in  users
        ]
    