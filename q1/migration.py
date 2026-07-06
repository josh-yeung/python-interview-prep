import stripe
from stripe import StripeClient
import json

# Point the SDK to your local stripe-mock server
client = StripeClient("sk_test_123", base_addresses={"api": "http://localhost:12111"})

def load_legacy_data(filepath):
    """Loads the JSON file and returns a list of dictionaries."""
    with open(filepath, 'r') as file:
        return json.load(file)

def run_migration():
    # 1. Load the data
    raw_data = load_legacy_data('legacy_data.json')
   
    # TODO: Implement the migration logic here

    filtered_results = [entry for entry in raw_data 
                        if entry["contact_email"] != None 
                        and entry["contact_email"] != "" 
                        and entry["account_balance_cents"] >= 0]
    
    output = []
    for entry in filtered_results:
        customer = client.v1.customers.create({
            "name": entry["full_name"],
            "email": entry["contact_email"],
            "metadata": {"legacy_id": entry["legacy_id"], "account_balance_cents": entry["account_balance_cents"]},
        })
        output.append({"legacy_id": entry["legacy_id"], "stripe_customer_id": customer.id})

    with open("migration_report.json", "w") as file:
        json.dump(output, file, indent=2)
    
run_migration()


