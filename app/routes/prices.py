from flask import Blueprint, request, jsonify
from ..models.grocery_item import GroceryItem
from ..models.store import Store
from ..db import db
from ..services.main import track_prices

prices_blueprint = Blueprint("prices", __name__)

def serialize_grocery_item(item):
    return {
        "id": item.id,
            "customName": item.customName,
            "url": item.url,
            "basePrice": item.basePrice,
            "store": item.store.value
    }

# get_prices function gets all prices and creates a json file with the prices for now
@prices_blueprint.route("/prices", methods=["GET"])
def get_prices():
    items=GroceryItem.query.all()
    serialized_items = [serialize_grocery_item(item) for item in items]
    track_prices(serialized_items)
# return serialized data