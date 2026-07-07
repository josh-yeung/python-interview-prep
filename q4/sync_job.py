import json
import requests

API_BASE = "https://api.logisticorp.com/v3"
HEADERS = {"Authorization": "Bearer wms_secret_token"}

def load_local_data():
    with open("local_inventory.json", 'r') as f:
        return json.load(f)
    
def string_formatter(name):
    first_three = name[:3]
    rest = name[3:]
    return (first_three + "-" + rest).upper()

def run_sync():
    local_items = load_local_data()
    print(f"Starting sync for {len(local_items)} items...")
    try:
        for item in local_items:
            item_name = string_formatter(item["name"])
            local_quantity = item["quantity"]
            item_url = f"{API_BASE}/inventory/{item_name}"
            response = requests.get(item_url,headers=HEADERS,params={"external_sku": item_name})
            """
            Response:
            {"data": {"sku": "SHO-SNEAKER", "current_stock": 45}}
            """
            if response.status_code == 200:
                remote_data = response.json()
                if remote_data["data"]["current_stock"] != local_quantity:
                    payload = {"stock": local_quantity}
                    requests.put(item_url,json=payload,headers=HEADERS)
            if response.status_code == 404:
                create_url = f"{API_BASE}/inventory"
                payload = {"item_details": {
                    "sku": item_name,
                    "stock": local_quantity
                },
                "source": "nightly_sync"
                }
                requests.post(API_BASE,json=payload,headers=HEADERS)
    except Exception as e:
        print("Error {e}")
        
        

if __name__ == "__main__":
    run_sync()
    