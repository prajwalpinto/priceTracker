import requests
import json
from bs4 import BeautifulSoup
from helper_module import find_value_in_json

def fetch_walmart_price(url,store):
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