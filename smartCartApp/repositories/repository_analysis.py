from bson import ObjectId
import pandas as pd
from collections import Counter
from datetime import datetime
from pymongo import DESCENDING

class RepositoryAnalysis:
    def __init__(self, db):
        self.db = db

    def get_user_purchase_stattistics(self, user_id):
        user_obj_id = ObjectId(user_id)
        purchases = list(self.db.purchases.find({"user_id": user_obj_id}))

        if not purchases:
            return {
                "total_purchases": 0,
                "total_spent": 0.0,
                "top_5_products": []
            }
        
        all_rows = []

        for purchase in purchases:
            for item in purchase["products"]:
                product = self.db.products.find_one({"_id": item["product_id"]})
                if product:
                      all_rows.append({
                            "product_name": product["name"],
                            "quantity": item["quantity"],
                            "price": item["price_at_purchase"]
                      })
        
        df = pd.DataFrame(all_rows)
        total_spent = (df["quantity"] * df["price"]).sum()
        top_5_products = df.groupby("product_name")["quantity"].sum().sort_values(ascending=False).head(5).index.tolist()

        return {
              "total_purchases": len(purchases),
              "total_spent": round(total_spent),
              "top_5_products": top_5_products 
        }
    
    def predict_next_products(self, user_id):
        user_obj_id = ObjectId(user_id)
        purchases = list(self.db.purchases.find({"user_id": user_obj_id}))

        if not purchases:
            return {"predict_products": []}
        
        all_products_ids = []

        for purchase in purchases:
            for item in purchase["products"]:
                all_products_ids.append(str(item["product_id"]))
        
        product_counts = Counter(all_products_ids)

        #We only filter products purchased more than once
        frequent_ids = [pid for pid, count in product_counts.items() if count > 1]

        predicted_products = []
        for pid in frequent_ids:
            product = self.db.products.find_one({"_id": ObjectId(pid)})
            if product: 
                predicted_products.append(product["name"])
        
        return {
            "predicted_products": predicted_products[:5]#top 5
        }

    
    def get_frequently_bought_together(self, product_id):
        product_obj_id = ObjectId(product_id)

        #Find all markets containing this product
        purchases = list(self.db.find({"products.product_id": product_obj_id}))

        other_products_ids = []

        for purchase in purchases:
            for item in purchase["products"]:
                pid = item["product_id"]
                if pid != product_obj_id:
                    other_products_ids.append({str(pid)})
        
        product_counter = Counter(other_products_ids)
        most_common_ids = [ObjectId(pid) for pid, _ in product_counter.most_common(5)]

        products = self.db.products.find({"_id": {"$in": most_common_ids}})
        result = [product["name"] for product in products]

        return{

            "frequently_bought_together": result
        }