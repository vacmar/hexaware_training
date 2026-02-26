import json
response = '''
{
  "order_id": 1001,
  "customer": {
    "name": "Ravi",
    "email": "ravi@example.com"
  },
  "items": [
    {"product": "Laptop", "qty": 1, "price": 55000},
    {"product": "Mouse",  "qty": 2, "price": 400}
  ]
}
'''
 
order = json.loads(response)
print(order["customer"]["name"])
print(order["items"][0]["product"])
print(order["items"][1]["price"])      
 
for item in order["items"]:
    total = item["qty"] * item["price"]
    print(f"{item['product']} Total: {total}")
    
'''
This looks like a comment
But it is actually a string
that is not assigned to anything
'''