user = {"name": "Bhuvaneswari", "age": 30, "city": "Chennai"}
 
import json
 
with open("user.json", "w") as file:
    json.dump(user, file, indent=2)
    
#user.json file will be created with the content of the user dictionary in JSON format.