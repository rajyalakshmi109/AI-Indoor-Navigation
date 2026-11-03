import pandas as pd
import numpy as np
import os

# Dataset location
DATA_PATH = "dataset/WiFi_Final_Dataset.xlsx"

# Output folder
os.makedirs("dataset/processed", exist_ok=True)

print("Loading Wi-Fi dataset...")

# Read original Excel file
df = pd.read_excel(
    DATA_PATH,
    sheet_name="Merged Observations"
)

print("\nOriginal dataset shape:", df.shape)

# Remove rows without BSSID
df = df.dropna(subset=["BSSID"])

# Remove readings explicitly marked invalid
df = df[df["rssi_valid"] != 0]

# Convert RSSI to numeric
df["RSSI_dBm"] = pd.to_numeric(
    df["RSSI_dBm"],
    errors="coerce"
)

df = df.dropna(subset=["RSSI_dBm"])

# Convert BSSID to string
df["BSSID"] = df["BSSID"].astype(str).str.lower().str.strip()

# Create unique scan identifier
df["scan_key"] = df["session"] + "_" + df["scan_id"]

print("\nCleaned observations:", len(df))

# Create Wi-Fi fingerprint matrix
fingerprints = df.pivot_table(
    index=["scan_key", "location_id", "location_name", "floor"],
    columns="BSSID",
    values="RSSI_dBm",
    aggfunc="median"
)

# Missing access points receive a weak signal value
fingerprints = fingerprints.fillna(-100)

# Save processed dataset
fingerprints.to_csv(
    "dataset/processed/scan_fingerprints.csv"
)

print("\nProcessed fingerprint shape:", fingerprints.shape)

print("\nLocation distribution:")
print(
    fingerprints.reset_index()["location_name"]
    .value_counts()
)

print("\nPreprocessing completed successfully!")