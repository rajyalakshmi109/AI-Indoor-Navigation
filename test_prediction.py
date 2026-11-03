import pandas as pd
import joblib
from location_prediction import predict_location

df = pd.read_csv("dataset/processed/scan_fingerprints.csv")

sample = df.iloc[0]

scan_readings = sample.drop(
    ["scan_key", "location_id", "location_name", "floor"]
).to_dict()

predicted_location, confidence = predict_location(scan_readings)

print("\n========== AI LOCATION PREDICTION ==========")
print("Actual Location:", sample["location_name"])
print("Predicted Location:", predicted_location)
print(f"Prediction Confidence: {confidence:.2f}%")
print("============================================")