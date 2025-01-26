
import datetime
from flask import jsonify
import json
from .walmart import fetch_walmart_price
from .loblaw import fetch_loblaw_price

file_path="./products.json"

def load_products():
    data=[]
    try:
        with open(file_path, "r") as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
    except json.JSONDecodeError:
        print(f"Error: The file {file_path} contains invalid JSON.")

def fetch_price(url, store):
    if store == "Walmart":
        return fetch_walmart_price(url, store)
    elif store == "Superstore" or store == "NoFrills":
        return fetch_loblaw_price(url, store)
    else:
        return "Invalid store selection."

def track_prices(products):
    price_data = []
    for product in products:
        product_info={}
        product_info["customName"] = product['customName']
        url = product['url']
        store = product['store']
        response = fetch_price(url,store)
        if response is not None:
            product_info["name"] = response["name"]
            product_info["store"] = store
            product_info["price"] = response["price"]
            product_info["priceDrop"] = product["basePrice"] - response["price"] > 0
            product_info["basePrice"] = product["basePrice"]
            product_info["url"] = url
            price_data.append(product_info)
            print(price_data)
        else:
            price_data.append({"name":"ERROR","price":"ERROR", "url": url,})
            print(price_data)
    
    creation_time = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    payload = {"created_at": creation_time, "data": price_data}
    return payload
    # Save to file or database
    # with open("prices.json", "a") as file:
        # creation_time = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        # payload = {"created_at": creation_time, "data": price_data}
        # json.dump(payload, file, indent=4)
        

if __name__ == "__main__":
    track_prices()
