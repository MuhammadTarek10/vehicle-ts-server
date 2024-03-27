# app.py
import requests
from flask import Flask, jsonify, request

app = Flask(__name__)

# Constants
VALID_CAPACITIES = {"low", "medium", "high"}


@app.route("/")
def working():
    return "Working!"


@app.route("/submit", methods=["POST"])
def submit():
    if request.method == "POST":
        try:
            data = request.json

            # Extract data
            device_id = data["id"]
            lat = data["data"]["lat"]
            lng = data["data"]["lng"]
            name = data["data"].get("name", "Vehicle")
            capacity = data["data"].get("capacity", "low")
            speed = data["data"].get("speed", 0)

            # Validate data format
            if not (
                isinstance(device_id, str)
                and isinstance(lat, (int, float))
                and isinstance(lng, (int, float))
            ):
                return (
                    jsonify(
                        {
                            "error": "Invalid data format. 'id' must be a string, 'lat' and 'lng' must be numbers"
                        }
                    ),
                    400,
                )

            # Validate capacity field
            if capacity.lower() not in VALID_CAPACITIES:
                return (
                    jsonify(
                        {
                            "error": "Invalid capacity value. Must be 'low', 'medium', or 'high'."
                        }
                    ),
                    400,
                )

            # Validate speed field
            if not isinstance(speed, int) or speed < 0:
                return (
                    jsonify(
                        {
                            "error": "Invalid speed value. Must be a non-negative integer."
                        }
                    ),
                    400,
                )

            # Prepare response data
            response_data = {
                "id": device_id,
                "lat": lat,
                "lng": lng,
                "name": name,
                "capacity": capacity,
                "speed": speed,
            }

            # Make PUT request
            put_url = f"https://vehicle-ts-default-rtdb.firebaseio.com/{device_id}.json"
            put_data = {
                "lat": lat,
                "lng": lng,
                "name": name,
                "capacity": capacity,
                "speed": speed,
            }
            response = requests.put(put_url, json=put_data)

            if response.ok:
                return jsonify(response_data)
            else:
                return (
                    jsonify(
                        {"error": f"Error in PUT request - {response.status_code}"}
                    ),
                    500,
                )

        except Exception as e:
            return jsonify({"error": f"Invalid request - {str(e)}"}), 400

    else:
        return "Invalid request method"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=33507)
