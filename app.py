from flask import Flask, jsonify, request
import json
# Intitialise the app
app = Flask(__name__)

def read_json(filename="data.json"):
    with open(filename,"r") as read_file:
        data = json.load(read_file)
        return data
def write_json(new_name,filename="data.json"):
    with open(filename,"r+") as file:
        file_data = json.load(file)
        file_data["result"]["nama"] = new_name
        file.seek(0)
        json.dump(file_data,file,indent=4)
        file.truncate()
# Define what the app does
@app.get("/")
def index():
    data = read_json()
    return jsonify(data)

@app.get("/editName")
def editName():
    name = request.args.get("name")
    write_json(name)
    data = read_json()
    return jsonify(data)