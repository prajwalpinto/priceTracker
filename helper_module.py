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

def call_api(base_url, params=None, headers=None, method="GET"):
    import requests

    try:
        if method.upper() == "GET":
            response = requests.get(base_url, params=params, headers=headers)
        elif method.upper() == "POST":
            response = requests.post(base_url, json=params, headers=headers)
        else:
            return f"Unsupported HTTP method: {method}"

        # Check for HTTP success
        if response.ok:
            return response.json()  # Parse JSON data
        else:
            return {
                "error": f"HTTP {response.status_code}",
                "message": response.text
            }
    except requests.RequestException as e:
        return {"error": "RequestException", "message": str(e)}
    