from bson import ObjectId
from smartCartApp.repositories.repository_cart import RepositoryCart

class RepositoryPurchase:
    def __init__(self, db):
        self.db = db
        self.cart_collection = db["carts"]
        self.purchase_collection = db["purchases"]
    
    def purchase_cart(self, user_id):
        try:
            cart= self.cart_collection.find_one({"user_id": ObjectId(user_id)})
            if not cart or not cart.get("products"):
                return {"error": "Cart is empty or does not exist"}, 400
            
            purchased_items =[]
            for item in cart["products"]:
                purchased_items.append({
                    "product_id": item["product_id"],
                    "quantity": item["quantity"],
                    "price_at_purchase": float(item["price"])
                })
        
            purchase_data = {
                "user_id": ObjectId(user_id),
                "products": purchased_items,
                "price_at_purchase": float(sum(item["price"] * item["quantity"] for item in cart["products"]))
            }
            
            result =  self.purchase_collection.insert_one(purchase_data)

            #Clear the cart after purchase
            repo_cart = RepositoryCart(self.db)
            repo_cart.clear_cart(user_id)
            
            return {"message": "Purchase completed successfully"}, 200
        except Exception as ex:
            return {"error": str(ex)}, 500