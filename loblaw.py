
from helper_module import call_api, find_value_in_json
from dotenv import load_dotenv
import datetime
import os
load_dotenv()
def call_loblaw_api(url,store):
    headers = {
        "x-apikey":os.getenv("SUPERSTORE_API_KEY")
    }

    params = {
        "lang": "en",
        "date": datetime.datetime.now().strftime("%d%m%Y"),
        "pickupType": "STORE",
        "storeId":os.getenv("SUPERSTORE_STORE_ID") if store=="Superstore" else os.getenv("NOFRILLS_STORE_ID"),
        "banner":"rass" if store=="Superstore" else "nofrills"
    }
    response = call_api(url, params, headers, "GET")
    return response

def fetch_loblaw_price(url, store):
    response = call_loblaw_api(url,store)
    if response.get("error"):
        return response["error"]
    else:
        data = response
        if data:
            name = find_value_in_json(data, "name")
            price_data = find_value_in_json(data, "offers")
            price = price_data[0]["price"]["value"]    
            return {"name": name, "price": float(price)}
        else:
            print("Data not found in the superstore response.")