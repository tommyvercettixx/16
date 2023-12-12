import json

def get_profiles_from_file():
    with open("data.json", "r") as f:
        return json.load(f)
    
def set_profiles_to_file():
    with open("data.json", "w") as f:
        json.dump(data, f)

def jsonify_response(obj, message="Request was handled successfully"):
    return {
        "message": message,
        "result": obj
    }