import json

student = {
    "name": "John Doe",
    "age": 21,
    "courses": ["Math", "Science", "History"],
    "is_graduated": False
}

print(student)

json_str = json.dumps(student)

print(json_str) # everything is converted to string

print(type(json_str)) # <class 'str'>

print(json.dumps(student, indent=4)) # pretty print with indentation (space at the beginning of each line)

print(json.loads(json_str)) # convert json string back to python dictionary

print(type(json.loads(json_str))) # <class 'dict'>