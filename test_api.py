import pandas as pd
import joblib
import json

from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError


# Project directory
BASE_DIR = Path(__file__).resolve().parent


# Load cleaned Wi-Fi fingerprint dataset
df = pd.read_csv(
    BASE_DIR / "dataset" / "processed" /
    "scan_fingerprints_cleaned.csv"
)


# Load model feature columns
feature_columns = joblib.load(
    BASE_DIR / "models" / "feature_columns.pkl"
)


# Select one sample for testing
sample = df.iloc[0]


# Prepare only detected Wi-Fi readings
scan_readings = {}

for bssid in feature_columns:

    value = sample[bssid]

    if pd.notna(value):

        rssi = float(value)

        # Exclude missing signals and invalid zero readings
        if -100 < rssi < 0:
            scan_readings[bssid] = rssi


# Display number of detected access points
print("\nDetected matching access points:", len(scan_readings))


# Prepare API request
payload = json.dumps({
    "scan_readings": scan_readings
}).encode("utf-8")


request = Request(
    "http://127.0.0.1:5000/predict",
    data=payload,
    headers={
        "Content-Type": "application/json"
    },
    method="POST"
)


# Send request and receive prediction
print("\n========== API PREDICTION TEST ==========")

try:

    with urlopen(request, timeout=15) as response:

        result = json.loads(
            response.read().decode("utf-8")
        )

        print("\nAPI Response:")
        print(json.dumps(result, indent=4))

        print("\nActual Location:")
        print(sample["location_name"])

        print("\nPredicted Location:")
        print(result.get("predicted_location"))

        print("\nPrediction Confidence:")
        print(result.get("confidence"), "%")

        print(
            "\nMatched Access Points:",
            result.get("matched_access_points")
        )

except HTTPError as error:

    print("\nHTTP Error:", error.code)

    print(error.read().decode("utf-8"))

except URLError as error:

    print("\nConnection Error:", error.reason)

except Exception as error:

    print("\nUnexpected Error:", error)


print("\n=========================================")