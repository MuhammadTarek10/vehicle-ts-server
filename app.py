# app.py
import requests
from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route("/")
def working():
    return "Working!"


@app.route("/submit", methods=["POST"])
def submit():
    if request.method == "POST":
        try:
            data = request.json
            device_id = data["id"]
            lat = data["data"]["lat"]
            lng = data["data"]["lng"]
            try:
                name = data["data"]["name"]
            except:
                name = "Vehicle"

            response_data = {
                "id": device_id,
                "lat": lat,
                "lng": lng,
                "name": name,
            }

            # Validate input
            if not device_id or not lat or not lng:
                return jsonify({"error": "Invalid input data"}), 400

            # Make PUT request
            put_url = f"https://vehicle-ts-default-rtdb.firebaseio.com/{device_id}.json"
            put_data = {"lat": lat, "lng": lng, "name": name}
            response = requests.put(put_url, json=put_data)

            if response.status_code == 200:
                return jsonify(response_data)
            else:
                return (
                    jsonify(
                        {"error": f"Error in PUT request - {response.status_code}"}
                    ),
                    500,
                )
        except Exception as e:
            return jsonify({"error": f"Invalid JSON format - {str(e)}"}), 400
    else:
        return "Invalid request method"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=33507)
