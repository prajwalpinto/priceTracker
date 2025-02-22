from flask import Flask
from app.db import db
from .routes.grocery_item import grocery_blueprint
from.routes.prices import prices_blueprint
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///grocery.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    CORS(app)
    
    db.init_app(app)
    
    # Register blueprints
    app.register_blueprint(grocery_blueprint)
    app.register_blueprint(prices_blueprint)
    
    return app
