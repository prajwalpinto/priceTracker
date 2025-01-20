from flask import Blueprint, request, jsonify
from ..models.grocery_item import GroceryItem
from ..models.store import Store
from ..db import db

grocery_blueprint = Blueprint("grocery", __name__)

def validate_store(store_name):
    try:
        return Store(store_name)
    except ValueError:
        return None

@grocery_blueprint.route("/api/items", methods=["GET"])
def get_items():
    items = GroceryItem.query.all()
    return jsonify([ 
        {
            "id": item.id,
            "customName": item.customName,
            "url": item.url,
            "basePrice": item.basePrice,
            "store": item.store.value
        } for item in items]), 200

@grocery_blueprint.route("/api/items/<int:item_id>", methods=["GET"])
def get_grocery_item(item_id):
    item = GroceryItem.query.get(item_id)
    if not item:
        return jsonify({"error": "Item not found"}), 404

    return jsonify({
        "id": item.id,
            "customName": item.customName,
            "url": item.url,
            "basePrice": item.basePrice,
            "store": item.store.value
    }), 200

@grocery_blueprint.route("/api/items", methods=["POST"])
def add_item():
    data = request.get_json()
    if not data.get("customName") or not data.get("url") or not data.get("basePrice"):
        return jsonify({"error": "Invalid input"}), 400
    store = validate_store(data.get("store"))
    if not store:
        return jsonify({"error": "Invalid store name"}), 400
    
    new_item = GroceryItem(
        customName=data["customName"], 
        url=data["url"], 
        basePrice=data["basePrice"],
        store=store
    )
    db.session.add(new_item)
    db.session.commit()
    return jsonify({"message": "Grocery item created", "item": new_item.id}), 201

@grocery_blueprint.route("/api/items/<int:item_id>", methods=["PUT"])
def update_item(item_id):
    data = request.get_json()
    item = GroceryItem.query.get(item_id)
    if not item:
        return jsonify({"error": "Item not found"}), 404
    if "store" in data:
        store = validate_store(data["store"])
        if not store:
            return jsonify({"error": "Invalid store name"}), 400
        item.store = store
    
    item.url = data.get("url", item.url)
    item.customName = data.get("customName", item.customName)
    item.basePrice = data.get("basePrice", item.basePrice)
    db.session.commit()
    return jsonify({"message": "Grocery item updated"}), 200

@grocery_blueprint.route("/api/items/<int:item_id>", methods=["DELETE"])
def delete_item(item_id):
    item = GroceryItem.query.get(item_id)
    if not item:
        return jsonify({"error": "Item not found"}), 404
    
    db.session.delete(item)
    db.session.commit()
    return jsonify({"message": "Item deleted"}), 200
