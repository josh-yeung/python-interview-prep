import stripe
from simulated_framework import request, Response
from simulated_database import db

stripe.api_key = "sk_test_123"
ENDPOINT_SECRET = "whsec_abc123" # The secret used to verify webhooks

def handle_webhook():
    """
    Endpoint route: POST /stripe-webhook
    """
    raw_payload = request.get_raw_body()
    sig_header = request.headers.get("Stripe-Signature")

    # 1. Verify the signature
    try:
        event = stripe.Webhook.construct_event(
            payload=raw_payload, 
            sig_header=sig_header, 
            secret=ENDPOINT_SECRET
        )
    except (stripe.error.SignatureVerificationError, ValueError) as error:
        print("HTTP 400 Bad Request", error)
        return Response(status=400)
   
    # 2. Check idempotency
    if db.processed_events.exists(event.id):
        return Response(status=200)

    # 3. Route the event and trigger business logic
    try:
        order_id = event.data.object.metadata.order_id
        if event.type == "payment_intent.succeeded":
            db.orders.fulfill(order_id=order_id)
        if event.type == "payment_intent.payment_failed":
            db.orders.mark_failed(order_id=order_id)
        db.processed_events.insert(event_id=event.id)
    except Exception as e:
        return Response(status=500)

    # 4. Return the appropriate HTTP response
    return Response(status=200)