from bson import ObjectId
from datetime import datetime
from routes import db
from model import carts
from exceptions.smartCart_exceptions import DatabaseException, CartNotFound, InvalidProductExcepton
from pymongo import ReturnDocument
import hashlib
import os


# carts_collection = db["carts"]
# products_collection = db["products"]
# users_collection = db["users"]

class RepositoryCart:
    def __init__(self, db):
        self.db = db
        self.carts_collection = db["carts"]
        self.products_collection = db["products"]
        self.users_collection = db["users"]

    @staticmethod
    def generate_product_id(name, price):
        # Generate a unique product ID based on name and price
        # unique_str = f"{name}_{price}"

        # random_str = os.urandom(6).hex()
        # return hashlib.md5(unique_str.encode()).hexdigest()[:10] + random_str
        return os.urandom(12).hex() 
        # + hashlib.md5(f"{name}_{price}".encode()).hexdigest()[:10]
   
    def create_cart(self, user_id):
        cart = {
            "user_id": ObjectId(user_id),
            "products": [],
            "created_at": datetime.utcnow()
        }

        result = self.carts_collection.insert_one(cart)
        return str(result.inserted_id)
    
    
    def get_cart(self, user_id):
        try:
            cart = self.carts_collection.find_one({"user_id": ObjectId(user_id)})
            return cart
        except Exception as e:
            raise DatabaseException("Error fetching cart from database.") from e
    

    def add_product(self, user_id, product_id, quantity=1):

        user_id = ObjectId(user_id)
        product_id = ObjectId(product_id)

        #Check if the product exists
        product = self.products_collection.find_one({"_id": product_id})
        if not product:
            raise InvalidProductExcepton("Product not found.")
        
        #Look for existing cart or create a new one
        cart = self.carts_collection.find_one({"user_id": user_id})
        if not cart:
            cart = {
                "user_id": user_id,
                "products": [{
                    "product_id": product_id,
                    "name": product["name"],
                    "price": product["price"],
                    "quantity": quantity
                }],
                "created_at": datetime.utcnow()
            }
            self.carts_collection.insert_one(cart)
            return {"message": "Cart created and product added."}
        
        # Check if the product already exists in the cart
        existing_product = next((p for p in cart["products"] if p["product_id"] == product_id), None)
        if existing_product:
            #Update quantity. ($inc = increment)
            self.carts_collection.update_one(
                {"_id": cart["_id"], "products.product_id": product_id},
                {"$inc": {"products.$.quantity": quantity}}
            )
            return {"message": "Product quantity updated."}
        else:
            #Add new product to cart
            self.carts_collection.update_one(
                {"_id": cart["_id"]},
                {"$push": {
                    "products": {
                        "product_id": product_id,
                        "name": product["name"],
                        "price": product["price"],
                        "quantity": quantity
                    }
                }}
            )
            return {"message": "Product added to cart."}
        
        
    
    def remove_product(self, user_id, product_id):
        self.carts_collection.update_one(
            {"user_id": user_id},
            {
                "$pull": {
                    "products": {
                        "product_id": product_id
                    }
                }
            }
        )

    
    def update_quantity(self, user_id, product_id, new_quantity):
        self.carts_collection.update_one(
            {
                "user_id": ObjectId(user_id),
                "products.prodect_id": ObjectId(product_id)
            },
            {
                "$set": {
                    "products.$.quantity": new_quantity
                }
            }
        )

    
    def clear_cart(self, user_id):
        self.carts_collection.update_one(
            {"user_id": ObjectId(user_id)},
            {"$set": {"products": []}}
        )


    
    def delete_all_carts(self, user_id):
        self.carts_collection.delete_many({"user_id": ObjectId(user_id)})
    

    def delet_product_from_cart(self, user_id, product_id):
        result = self.carts_collection.update_one(
            {"user_id": ObjectId(user_id)},
            {"$pull": {"products": {"product_id": ObjectId(product_id)}}}
        )
        return result 