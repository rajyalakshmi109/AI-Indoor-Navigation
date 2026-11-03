import pandas as pd

file_path = "dataset/processed/scan_fingerprints.csv"

df = pd.read_csv(file_path)

label_mapping = {
    "First-Floor Computer Centre Entrance":
        "First Floor Computer Centre Entrance",

    "First-Floor Computer Lab 2":
        "First Floor Computer Lab 2",

    "First-Floor Staircase Landing":
        "First Floor Staircase Landing",

    "Ground Floor Study Hall Entrance":
        "Ground Floor Study Hall 2 Entrance",

    "Library Hall 2 Centre":
        "Ground Floor Library Hall 2 Centre",

    "Library Hall 2 Entrance":
        "Ground Floor Library Hall 2 Entrance",

    "Ojah Ma'am's Cabin":
        "First Floor Ojah Ma'am's Cabin"
}

df["location_name"] = df["location_name"].replace(label_mapping)

df.to_csv(file_path, index=False)

print("Location labels standardized successfully!")

print("\nUpdated location labels:")

for location in sorted(df["location_name"].unique()):
    print(location)