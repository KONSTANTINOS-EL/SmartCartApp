from flask import Flask
from pymongo import MongoClient
from bson.objectid import ObjectId
import json

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return super().default(o)

server = Flask(__name__)
server.json_encoder = JSONEncoder

client = MongoClient('localhost:27017')
db = client['smart_cart_db']

from smartCartApp.routes.cart_routes import product_routes, cart_routes
from smartCartApp.routes.user_routes import user_routes
from smartCartApp.routes.webScraping_routes import webScraping_product_routes
from smartCartApp.routes.purchase_routes import purchase_routes
from smartCartApp.routes.analysis_routs import analysis_routes
from smartCartApp.routes.ai_routes import ai_route

server.register_blueprint(product_routes)
server.register_blueprint(cart_routes)
server.register_blueprint(user_routes)
server.register_blueprint(webScraping_product_routes)
server.register_blueprint(purchase_routes)
server.register_blueprint(analysis_routes)
server.register_blueprint(ai_route)
