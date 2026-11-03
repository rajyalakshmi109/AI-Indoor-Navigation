from flask import Flask, request, jsonify
from datetime import datetime

from location_prediction import predict_location, feature_columns
from navigation import find_shortest_route
from directions import generate_instructions


# ==================================================
# INITIALIZE FLASK APPLICATION
# ==================================================

app = Flask(__name__)


# ==================================================
# AVAILABLE DESTINATIONS
# ==================================================

LOCATIONS = [
    "Ground Floor Library Entrance",
    "Ground Floor Study Hall 2 Entrance",
    "Ground Floor Library Hall 2 Entrance",
    "Ground Floor Staircase Entrance",
    "Ground Floor Study Hall Centre",
    "Ground Floor Library Hall 2 Centre",
    "First Floor Staircase Landing",
    "First Floor Computer Centre Entrance",
    "First Floor Computer Lab 2",
    "First Floor Corridor Outside Lab 2",
    "First Floor Ojah Ma'am's Cabin"
]


# ==================================================
# STORE LATEST LIVE LOCATION
# ==================================================

latest_live_location = None


def update_latest_location(
    predicted_location,
    confidence,
    matched_access_points
):
    global latest_live_location

    latest_live_location = {
        "status": "success",
        "current_location": str(predicted_location),
        "confidence": round(float(confidence), 2),
        "matched_access_points": matched_access_points,
        "total_model_features": len(feature_columns),
        "last_updated": datetime.now().astimezone().isoformat()
    }


# ==================================================
# PROCESS WI-FI SCAN READINGS
# ==================================================

def process_scan_readings(scan_readings):

    if not isinstance(scan_readings, dict):
        raise ValueError(
            "scan_readings must be a dictionary."
        )

    normalized_readings = {}

    for bssid, rssi in scan_readings.items():

        bssid = str(bssid).strip().lower()

        if bssid not in feature_columns:
            continue

        try:
            rssi = float(rssi)

        except (TypeError, ValueError):
            continue

        if -100 < rssi < 0:
            normalized_readings[bssid] = rssi

    if not normalized_readings:
        raise ValueError(
            "No matching Wi-Fi access points found."
        )

    return normalized_readings


# ==================================================
# HEALTH CHECK
# ==================================================

@app.route("/health", methods=["GET"])
def health():

    return jsonify({
        "status": "success",
        "message": "AI Indoor Navigation API is running!"
    })


# ==================================================
# AVAILABLE DESTINATIONS
# ==================================================

@app.route("/destinations", methods=["GET"])
def destinations():
    user_destinations = [
        location for location in LOCATIONS
        if location != "First Floor Corridor Outside Lab 2"
    ]

    return jsonify({
        "status": "success",
        "destinations": user_destinations
    })



# ==================================================
# WI-FI LOCATION PREDICTION
# ==================================================

@app.route("/predict", methods=["POST"])
def predict():

    try:

        data = request.get_json(silent=True)

        if not isinstance(data, dict):
            return jsonify({
                "error": "Invalid JSON request."
            }), 400

        scan_readings = process_scan_readings(
            data.get("scan_readings")
        )

        predicted_location, confidence = predict_location(
            scan_readings
        )

        # Save latest live prediction
        update_latest_location(
            predicted_location,
            confidence,
            len(scan_readings)
        )

        return jsonify({
            "status": "success",
            "predicted_location": str(predicted_location),
            "confidence": round(float(confidence), 2),
            "matched_access_points": len(scan_readings),
            "total_model_features": len(feature_columns)
        })

    except ValueError as error:

        return jsonify({
            "status": "error",
            "message": str(error)
        }), 422

    except Exception as error:

        return jsonify({
            "status": "error",
            "message": str(error)
        }), 500


# ==================================================
# GET LATEST LIVE LOCATION
# ==================================================

@app.route("/live-location", methods=["GET"])
def live_location():

    if latest_live_location is None:

        return jsonify({
            "status": "waiting",
            "message": (
                "No live Wi-Fi scan received yet. "
                "Please scan using the Android application."
            )
        }), 404

    return jsonify(latest_live_location)


# ==================================================
# COMPLETE INDOOR NAVIGATION
# ==================================================

@app.route("/navigate", methods=["POST"])
def navigate():

    try:

        data = request.get_json(silent=True)

        if not isinstance(data, dict):

            return jsonify({
                "error": "Invalid JSON request."
            }), 400

        # Get Wi-Fi readings
        scan_readings = process_scan_readings(
            data.get("scan_readings")
        )

        # Get destination
        destination = data.get("destination")

        if not isinstance(destination, str):

            return jsonify({
                "error": "Please provide a valid destination."
            }), 400

        destination = destination.strip()

        if destination not in LOCATIONS:

            return jsonify({
                "error": "Destination not found.",
                "available_destinations": LOCATIONS
            }), 400

        # Predict current location
        predicted_location, confidence = predict_location(
            scan_readings
        )

        predicted_location = str(predicted_location)

        # Save latest live prediction
        update_latest_location(
            predicted_location,
            confidence,
            len(scan_readings)
        )

        # Check whether already at destination
        if predicted_location == destination:

            return jsonify({
                "status": "success",
                "current_location": predicted_location,
                "destination": destination,
                "confidence": round(float(confidence), 2),
                "matched_access_points": len(scan_readings),
                "route": [predicted_location],
                "approximate_distance_metres": 0,
                "walking_instructions": [
                    "You are already at your destination!"
                ]
            })

        # Calculate shortest route
        route, distance = find_shortest_route(
            predicted_location,
            destination
        )

        if not route:

            return jsonify({
                "status": "error",
                "message": "No route available."
            }), 404

        # Generate walking instructions
        instructions = generate_instructions(route)

        return jsonify({
            "status": "success",
            "current_location": predicted_location,
            "destination": destination,
            "confidence": round(float(confidence), 2),
            "matched_access_points": len(scan_readings),
            "route": route,
            "approximate_distance_metres": distance,
            "walking_instructions": instructions
        })

    except ValueError as error:

        return jsonify({
            "status": "error",
            "message": str(error)
        }), 422

    except Exception as error:

        return jsonify({
            "status": "error",
            "message": str(error)
        }), 500


# ==================================================
# START FLASK SERVER
# ==================================================

if __name__ == "__main__":

    print("====================================")
    print("AI INDOOR NAVIGATION API")
    print("====================================")

    print("Server starting on port 5000...")
    print("Health endpoint: /health")
    print("Prediction endpoint: /predict")
    print("Destinations endpoint: /destinations")
    print("Navigation endpoint: /navigate")
    print("Live location endpoint: /live-location")

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )