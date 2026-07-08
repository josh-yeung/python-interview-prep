import json
import uuid
from stripe import StripeClient

client = StripeClient("sk_test_123", base_addresses={"api": "http://localhost:12111"})

def load_cancellations(filepath):
    with open(filepath, 'r') as f:
        object = json.load(f)
        for o in object:
            o["ikey"] = uuid.uuid4()
        return object



def run_refund_job():
    orders_to_refund = load_cancellations("cancellations.json")
    print(f"Starting refund job for {len(orders_to_refund)} orders...")
    
    # TODO: Implement the refund logic here
    try:
        for orders in orders_to_refund:
            order_id = orders["order_id"]
            query = f"metadata['order_id']:'{order_id}'"
            response = client.v1.charges.search({"query": query})
            response = response.data[0]
            if not response:
                print("Warning no charge")
                continue
            if response.status == "requires_capture":
                client.v1.payment_intents.cancel(response["payment_intent"])
                with open("successful_refunds.txt", "a") as f:
                    f.write(f"Order {response.id} refunded via payment\n")
                
            else:
                refund = client.v1.refunds.create(
                    params={
                        "charge": response.id,
                        "reason": "requested_by_customer"
                    },
                    options={"idempotency_key": str(orders["ikey"])}
                )
                print(refund)
                with open("successful_refunds.txt", "a") as f:
                    f.write(f"Order {response.id} refunded via Refund ID: {refund.id}\n")
                
    except Exception as e:
        print(f"BAD! {e}")

    print("Refund job completed.")

if __name__ == "__main__":
    run_refund_job()