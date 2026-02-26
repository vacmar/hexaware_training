import json
def parse_json(raw):
    try:
        return json.loads(raw)
    except json.JSONDecodeError as e:
        print(f"Invalid JSON: {e}")
        return None
 
data = parse_json('{"name": "Arun"}')   # ✅ works
print(data)
data = parse_json('not json at all')    # ❌ handled gracefully
print(data)