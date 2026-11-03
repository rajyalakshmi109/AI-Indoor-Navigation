import pandas as pd
import pickle
import os

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

print("Loading processed Wi-Fi fingerprints...")

# Load dataset

df = pd.read_csv("dataset/processed/scan_fingerprints.csv")

# Separate features and target

X = df.drop(columns=[
"scan_key",
"location_id",
"location_name",
"floor"
])

y = df["location_name"]

# Handle missing values

X = X.fillna(-100)

# Split dataset

X_train, X_test, y_train, y_test = train_test_split(
X,
y,
test_size=0.2,
random_state=42,
stratify=y
)

print("Training Random Forest model...")

# Create model

model = RandomForestClassifier(
n_estimators=100,
random_state=42,
class_weight="balanced"
)

# Train model

model.fit(X_train, y_train)

# Predict

y_pred = model.predict(X_test)

# Evaluate

accuracy = accuracy_score(y_test, y_pred)

print("\nModel Accuracy:", round(accuracy * 100, 2), "%")

print("\nClassification Report:")
print(classification_report(y_test, y_pred, zero_division=0))

# Save model

os.makedirs("models", exist_ok=True)

with open("models/random_forest.pkl", "wb") as f:
   pickle.dump(model, f)

with open("models/feature_columns.pkl", "wb") as f:
   pickle.dump(list(X.columns), f)

print("\nRandom Forest model saved successfully!")
print("======================================")
