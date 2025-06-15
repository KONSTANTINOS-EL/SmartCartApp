from bson import ObjectId
from routes import db

products_collection = db.get_collection("products")
carts_collection = db["carts"]
purchases_collection = db["purchases"]

class RepositoryProducts:

    @staticmethod
    def insert_product(product):
        if not product:
            raise ValueError("Product must not be empty.")
        
        try:
            inserted_by_id = products_collection.insert_one(product).inserted_id
            return inserted_by_id
        except Exception as e:
            print(f"Error inserting product: {e}")
            raise

    @staticmethod
    def get_all_products():
        return list(products_collection.find())
    
    @staticmethod
    def get_by_id(product_id):
        return products_collection.find_one({"_id": ObjectId(product_id)})
        # return products_collection.insert_one({"_id": ObjectId(product_id)})
    
    @staticmethod
    def update(product_id, updates):
        if not product_id:
            raise ValueError("Product does not exist")
        return products_collection.update_one(
            {"_id": ObjectId(product_id)},
            {"$set": updates}
        )
    
    @staticmethod
    def delete(product_id):
        if not product_id:
            raise ValueError("Product does not exist")
        return products_collection.delete_one({"_id": ObjectId(product_id)})
    
    @staticmethod
    def delete_all():
        return products_collection.delete_many({})