from datetime import datetime
from bson import ObjectId

class Cart: 
    def __init__(self, user_id):
        self.user_id = ObjectId(user_id)
        self.products = []
        self.created_at = datetime.utcnow()

    
    def to_dict(self):
        return {
            "user_id": self.user_id,
            "products": self.products,
            "created_at": self.created_at
        }