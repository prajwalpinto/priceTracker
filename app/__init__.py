from flask import Flask
from app.db import db
from .routes.grocery_item import grocery_blueprint

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///grocery.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    
    db.init_app(app)
    
    # Register blueprints
    app.register_blueprint(grocery_blueprint)
    
    return app
