import json
from datetime import datetime, timedelta

api_response = '''
{
    "order_id": 1001,
    "customer": "Arun Kumar",
    "place_at": "2024-06-01T10:30:00Z",
    "items": [
        {"product": "Laptop", "qty": 1, "price": 55000},
        {"product": "Mouse",  "qty": 2, "price": 400}
    ],
    "status": "confirmed"
}
'''

order = json.loads(api_response)

placed_at = datetime.fromisoformat(order["place_at"].replace("Z", "+00:00"))
estimated_delivery = placed_at + timedelta(days=5)

total = sum(item["qty"] * item["price"] for item in order["items"])

order_summary = {
    "order_id": order["order_id"],
    "customer": order["customer"],
    "placed_at": placed_at.isoformat(),
    "estimated_delivery": estimated_delivery.isoformat(),
    "total_amount": f"₹{total}",
    "status": order["status"].upper()
}

print(json.dumps(order_summary, indent=2, ensure_ascii=False))