import pandas as pd
import joblib
import os

# Get project directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Load trained Random Forest model
model = joblib.load(
    os.path.join(BASE_DIR, "models", "random_forest.pkl")
)

# Load feature columns
feature_columns = joblib.load(
    os.path.join(BASE_DIR, "models", "feature_columns.pkl")
)


def predict_location(scan_readings):

    values = []

    for bssid in feature_columns:
        rssi = scan_readings.get(bssid, -100)

        try:
            rssi = float(rssi)
        except (TypeError, ValueError):
            rssi = -100

        values.append(rssi)

    input_data = pd.DataFrame(
        [values],
        columns=feature_columns
    )

    prediction = model.predict(input_data)[0]

    probabilities = model.predict_proba(input_data)[0]

    confidence = max(probabilities) * 100

    return prediction, confidence