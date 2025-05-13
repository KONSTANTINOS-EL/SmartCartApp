import uuid
class Products:
    def __init__(self, name, description, price, category, image_url):
        self.name = name
        self.description = description
        self.price = float(price)
        self.category = category
        self.image_url = image_url
        self.id = str(uuid.uuid4())
    
    def __eq__(self, other_value):
        return self.id == other_value.id
    
    def __repr__(self):
        return f"Products('{self.id}', '{self.name}', '{self.description}', {self.price}, {self.category}, {self.image_url})"
    
    def to_dict(self):
        return {
        "id": self.id,
        "name": self.name,
        "description": self.description,
        "price": self.price,
        "category": self.category,
        "image_url": self.image_url
        }
    
    def from_dict(self, data):
        self.id = data.get("id") if data.get("id") is not None else self.id
        self.name = data.get("name") if data.get("name") is not None else self.name
        self.description = data.get("description") if data.get("description") is not None else self.description
        self.price = data.get("price") if data.get("price") is not None else self.price
        self.category = data.get("category") if data.get("category") is not None else self.category
        self.image_url = data.get("image_url") if data.get("image_url") is not None else self.image_url

