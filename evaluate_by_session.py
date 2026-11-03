import pandas as pd
from pathlib import Path

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)

BASE_DIR = Path(__file__).resolve().parent

# Load dataset
df = pd.read_csv(
    BASE_DIR / "dataset" / "processed" / "scan_fingerprints.csv"
)

# Identify collection sessions
df["session"] = (
    df["scan_key"]
    .astype(str)
    .str.extract(r"^(Session\s+\d+)", expand=False)
)

# Load feature columns
import joblib

feature_columns = joblib.load(
    BASE_DIR / "models" / "feature_columns.pkl"
)

# Prepare input features
X = df[feature_columns].fillna(-100)
y = df["location_name"]

# Training data: Sessions 1 and 2
train_mask = df["session"].isin(["Session 1", "Session 2"])

# Testing data: Sessions 3 and 4
test_mask = df["session"].isin(["Session 3", "Session 4"])

X_train = X.loc[train_mask]
y_train = y.loc[train_mask]

X_test = X.loc[test_mask]
y_test = y.loc[test_mask]

# Train a fresh Random Forest model
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42,
    class_weight="balanced"
)

model.fit(X_train, y_train)

# Predict test locations
predictions = model.predict(X_test)

# Overall evaluation
accuracy = accuracy_score(y_test, predictions)

print("\n========== SESSION-BASED EVALUATION ==========")

print("\nTraining fingerprints:", len(X_train))
print("Testing fingerprints:", len(X_test))

print(f"\nOverall Accuracy: {accuracy * 100:.2f}%")

print("\nClassification Report:")

print(
    classification_report(
        y_test,
        predictions,
        labels=model.classes_,
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

# Evaluate each testing session separately
print("\n========== SESSION-WISE ACCURACY ==========")

for session in ["Session 3", "Session 4"]:

    mask = df.loc[X_test.index, "session"] == session

    session_actual = y_test.loc[mask]
    session_predicted = predictions[mask.to_numpy()]

    session_accuracy = accuracy_score(
        session_actual,
        session_predicted
    )

    print(
        f"{session}: {session_accuracy * 100:.2f}% "
        f"({len(session_actual)} samples)"
    )

# Display incorrect predictions
print("\n========== INCORRECT PREDICTIONS ==========")

for index, actual, predicted in zip(
    X_test.index,
    y_test,
    predictions
):

    if actual != predicted:

        print("\nScan Key:", df.loc[index, "scan_key"])
        print("Actual:", actual)
        print("Predicted:", predicted)

print("\n===========================================")