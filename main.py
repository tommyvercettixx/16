from flask import Flask, jsonify, request
from functions import jsonify_response, get_profiles_from_file, set_profiles_to_file
import random

app = Flask(__name__)

@app.route("/")
def index():
    return "Hello World"

@app.route("/profiles")
def get_profiles():
    result = get_profiles_from_file()
    return jsonify_response(result)

@app.route("/profiles/<int:id>")
def get_profile_by_id(id):
    profiles = get_profiles_from_file()
    for profile in profiles:
        if profile.get("id") == id:
            return jsonify_response(profile)
    return jsonify_response(None, message=f"There is no profile with ID: {id}")

@app.route("/profiles/create", methods=["POST"])
def create_profile():
    profiles = get_profiles_from_file()
    login = request.form["login"]

    for profile in profiles:
        if profile.get("login") == login:
            return jsonify_response(None, message="Login existed, creation has failed")
    
    account = request.form["account"]
    nat = request.form["nationality"]

    created_profile = {
        "id": random.randrange(1, 100_000),
        "login": login,
        "account": account,
        "nationality": nat
    }

    profiles.append(created_profile)
    set_profiles_to_file(profiles)

    return jsonify(created_profile)

@app.route("/profiles/update/<int:id>", methods=["POST"])
def update_profile_by_id(id):
    profiles = get_profiles_from_file()
    for profile in profiles:
        if profile.get("id") == id:
            for key in request.form:
                profile[key] = request.form[key]
            return jsonify_response(profile)
    return jsonify_response(None, message=f"Can't find profile with ID: {id}")

@app.route("/profiles/delete/<int:id>", methods=["POST"])
def delete_profile_by_id(id):
    profiles = get_profiles_from_file()
    
    index = None
    for i in range(len(profiles)):
        if profiles[i].get("id") == id:
            index = i
            break

    if index == None:
        return jsonify_response(False, message=f"Profile with ID: {id} was not detected")
    
    profiles.pop(index)
    set_profiles_to_file(profiles)

    return jsonify_response(True, message=f"Profile with ID: {id} was deleted")

if __name__ == '__main__':
    app.run(debug=True)