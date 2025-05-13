from datetime import datetime
from bson import ObjectId

class Purchase:
    def __init__(self, products):
        self.products = [
            {
                "product_id": ObjectId(product["product_id"]),
                "quantity": product["quantity"],
                "price_at_purchase": float(product["price_at_purchase"])
            }
            for product in products
        ]

        self.purchased_at = datetime.utcnow()
        self.total_price = self.calculate_total()

    def calculate_total(self):
        return round(sum(p["price_at_purchase"] * p["quantity"] for p in self.products), 2)

        