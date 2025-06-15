from flask import Flask
from pymongo import MongoClient
from bson.objectid import ObjectId
import json
import os

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return super().default(o)

server = Flask(__name__)
server.json_encoder = JSONEncoder

mongo_uri = os.getenv('MONGO_URI', "mongodb://mongo:27017")
client = MongoClient(mongo_uri)
db = client['smart_cart_db']

from routes.cart_routes import cart_routes
from routes.product_routes import product_routes
from routes.user_routes import user_routes
from routes.webScraping_routes import webScraping_product_routes
from routes.purchase_routes import purchase_routes
from routes.analysis_routs import analysis_routes
from routes.ai_routes import ai_route

server.register_blueprint(product_routes)
server.register_blueprint(cart_routes)
server.register_blueprint(user_routes)
server.register_blueprint(webScraping_product_routes)
server.register_blueprint(purchase_routes)
server.register_blueprint(analysis_routes)
server.register_blueprint(ai_route)
