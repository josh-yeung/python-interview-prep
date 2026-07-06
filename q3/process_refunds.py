import json
import uuid
from stripe import StripeClient

client = StripeClient("sk_test_123", base_addresses={"api": "http://localhost:12111"})

def load_cancellations(filepath):
    with open(filepath, 'r') as f:
        return json.load(f)

def run_refund_job():
    orders_to_refund = load_cancellations("cancellations.json")
    print(f"Starting refund job for {len(orders_to_refund)} orders...")
    
    # TODO: Implement the refund logic here
            
    print("Refund job completed.")

if __name__ == "__main__":
    run_refund_job()