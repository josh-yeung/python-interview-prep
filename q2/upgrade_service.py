import json
from stripe import StripeClient
from datetime import date

# System constants
PRO_TIER_PRICE_ID = "price_pro_tier_999"

client = StripeClient("sk_test_123", base_addresses={"api": "http://localhost:12111"})

def load_json_file(filepath):
    with open(filepath, 'r') as f:
        return json.load(f)
    
def getPromotions(filepath):
    with open(filepath, "r") as f:
        promotion = json.load(f)
        stripe_coupon_id = promotion["stripe_coupon_id"]
        minimum_account_age_days = promotion["eligibility_rules"]["minimum_account_age_days"]
        return stripe_coupon_id, minimum_account_age_days
    
def auditLogging(filepath, object):
    with open(filepath, "a") as file:
        dateToday = date.today()
        user_id = object["id"]
        price = object["items"]["data"][0]["price"]["unit_amount"]
        file.write(f"{dateToday} User {user_id} upgraded for {price}\n")

def process_upgrades(requests_filepath):
    """
    Main job runner. Iterates through requests and upgrades them to the Pro tier.
    """
    requests = load_json_file(requests_filepath)
    success_count = 0
    stripe_coupon_id, minimum_account_age_days = getPromotions("promotions.json")
    
    print(f"Found {len(requests)} upgrade requests.")
    
    for req in requests:
        try:
            if req["account_age_days"] >= minimum_account_age_days:
                subscription = client.v1.subscriptions.update(
                    req["stripe_subscription_id"],
                    {
                    "items": [{
                        "id": req["stripe_subscription_item_id"],
                        "price": PRO_TIER_PRICE_ID
                    }]},
                    {"coupon": stripe_coupon_id}
                )
                print(f"Successfully upgraded user with coupon: {req['user_id']}")
                success_count += 1

                auditLogging("discount_audit_log.txt", subscription)

            else:
            # EXISTING LOGIC: Blindly apply the upgrade
            #             
                client.v1.subscriptions.update(
                    req["stripe_subscription_id"],
                    {
                    "items": [{
                        "id": req["stripe_subscription_item_id"],
                        "price": PRO_TIER_PRICE_ID
                    }]
                    }
                )
                print(f"Successfully upgraded user: {req['user_id']}")
                success_count += 1
            
        except Exception as e:
            print(f"Failed to upgrade user {req['user_id']}. Error: {e}")

    print(f"Job complete. {success_count}/{len(requests)} processed.")

if __name__ == "__main__":
    process_upgrades("upgrade_requests.json")