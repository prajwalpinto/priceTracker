import requests
from bs4 import BeautifulSoup
import datetime
import json

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



def find_value_in_json(data, target_key):
    if isinstance(data, dict):
        for key, value in data.items():
            if key == target_key:
                return value
            if isinstance(value, (dict, list)):
                result = find_value_in_json(value, target_key)
                if result is not None:
                    return result
    elif isinstance(data, list):
        for item in data:
            result = find_value_in_json(item, target_key)
            if result is not None:
                return result
    return None

def fetch_price(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        script_tag = soup.find("script", {"type": "application/ld+json"})  # Adjust if needed

        if script_tag:
            # Step 4: Extract JSON data
            try:
                json_data = json.loads(script_tag.string)  # Parse the JSON content
                name = find_value_in_json(json_data, "name")
                price = find_value_in_json(json_data, "price")
                return {"name": name, "price": float(price)}
                
                # print(json.dumps(json_data, indent=4))  # Pretty-print the JSON
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON: {e}")
        else:
            print("No matching <script> tag found.")
            
        return None

def track_prices():
    price_data = []
    products = load_products()
    for product in products:
        product_info={}
        product_info["customName"] = product['customName']
        url = product['url']
        response = fetch_price(url)
        if response is not None:
            product_info["price"] = response["price"]
            product_info["priceDrop"] = product["basePrice"] - response["price"] > 0
            product_info["basePrice"] = product["basePrice"]
            product_info["name"] = response["name"]
            product_info["url"] = url
            price_data.append(product_info)
        else:
            price_data.append({"name":"ERROR","price":"ERROR", "url": url,})

    # Save to file or database
    with open("walmart_prices.txt", "a") as file:
        file.write(f"{datetime.datetime.now()} - {price_data}\n")

if __name__ == "__main__":
    track_prices()
