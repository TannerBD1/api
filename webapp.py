'''This app is going to create the basic structure that hosts an api'''
#   imports
from flask import Flask, jsonify, request
#   create app
app = Flask(__name__)

#   Insert data from database
items = [
    {"id": 1, "name": "fridge"},
    {"id": 2, "name": "freezer"},
    {"id": 3, "name": "dry"},
]
next_id = 4

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200

@app.route("/items", methods=["GET"])
def list_items():
    return jsonify(items), 200

@app.route("/items/<int:item_id>", methods=["GET"])
def get_item(item_id):
    for item in items:
        if item["id"] == item_id:
            return jsonify(item), 200
    return jsonify({"error": "Not found"}), 404

@app.route("/items", methods=["POST"])
def create_item():
    global next_id
    data = request.get_json(silent=True) or {}
    name = data.get("name")
    if not name:
        return jsonify({"error": "Field 'name' is required"}), 400
    
    item = {"id": next_id, "name": name}
    next_id += 1
    items.append(item)
    return jsonify(item), 201

@app.route("/items/<int:item_id>", methods=["DELETE"])
def delete_item(item_id):
    global items
    new_items = [i for i in items if i["id"] != item_id]
    if len(new_items) == len(items):
        return jsonify({"error": "Not found"}), 404
    items = new_items
    return "", 204

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
