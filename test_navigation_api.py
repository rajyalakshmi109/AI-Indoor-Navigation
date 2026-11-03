import pandas as pd
import joblib
import json
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

# Project directory

BASE_DIR = Path(__file__).resolve().parent

# Load dataset

df = pd.read_csv(
BASE_DIR / "dataset" / "processed" / "scan_fingerprints_cleaned.csv"
)

# Load feature columns

feature_columns = joblib.load(
BASE_DIR / "models" / "feature_columns.pkl"
)

# Select sample

sample = df.iloc[0]

# Prepare Wi-Fi readings

scan_readings = {}

# Prepare Wi-Fi readings
scan_readings = {}

for bssid in feature_columns:
    value = sample[bssid]

    if pd.notna(value):
        rssi = float(value)

        if -100 < rssi < 0:
            scan_readings[bssid] = rssi

print("\nDetected matching access points:", len(scan_readings))

# Destination

destination = "Ground Floor Library Entrance"

# Prepare request

payload = json.dumps({
"scan_readings": scan_readings,
"destination": destination
}).encode("utf-8")

request = Request(
"http://127.0.0.1:5000/navigate",
data=payload,
headers={"Content-Type": "application/json"},
method="POST"
)

print("\n========== NAVIGATION API TEST ==========")

try:
    with urlopen(request, timeout=15) as response:
        result = json.loads(response.read().decode("utf-8"))

        print("\nAPI RESPONSE:")
        print(json.dumps(result, indent=4))

        print("\nACTUAL LOCATION:")
        print(sample["location_name"])

        print("\nPREDICTED LOCATION:")
        print(result.get("current_location"))

        print("\nDESTINATION:")
        print(result.get("destination"))

        print("\nCONFIDENCE:")
        print(result.get("confidence"), "%")

        print("\nMATCHED ACCESS POINTS:")
        print(result.get("matched_access_points"))

        print("\nSHORTEST ROUTE:")
        for index, location in enumerate(result.get("route", []), start=1):
            print(f"{index}. {location}")

        print("\nAPPROXIMATE DISTANCE:")
        print(result.get("approximate_distance_metres"), "metres")

        print("\nWALKING INSTRUCTIONS:")
        for index, instruction in enumerate(
            result.get("walking_instructions", []), start=1
        ):
            print(f"{index}. {instruction}")

        print("\nNAVIGATION STATUS:")
        print(result.get("status"))

except HTTPError as error:
    print("\nHTTP ERROR:", error.code)
    print(error.read().decode("utf-8"))

except URLError as error:
    print("\nCONNECTION ERROR:", error.reason)

except Exception as error:
    print("\nUNEXPECTED ERROR:", error)

print("\n=========================================")