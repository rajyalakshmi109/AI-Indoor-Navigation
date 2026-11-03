import pandas as pd
import joblib
import os

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix


# Project directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Load dataset
df = pd.read_csv(
    os.path.join(BASE_DIR, "dataset", "processed", "scan_fingerprints.csv")
)

# Load trained model and feature columns
model = joblib.load(
    os.path.join(BASE_DIR, "models", "random_forest.pkl")
)

feature_columns = joblib.load(
    os.path.join(BASE_DIR, "models", "feature_columns.pkl")
)

# Prepare features and labels
X = df[feature_columns].fillna(-100)
y = df["location_name"]

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# Predict locations
predictions = model.predict(X_test)

# Calculate accuracy
accuracy = accuracy_score(y_test, predictions)

print("\n========== MODEL EVALUATION ==========")

print(f"\nOverall Accuracy: {accuracy * 100:.2f}%")

print("\nClassification Report:")

print(
    classification_report(
        y_test,
        predictions,
        zero_division=0
    )
)

print("\nConfusion Matrix:")

print(
    confusion_matrix(
        y_test,
        predictions,
        labels=model.classes_
    )
)

print("\nLocation Labels:")

for label in model.classes_:
    print(label)

print("\n======================================")