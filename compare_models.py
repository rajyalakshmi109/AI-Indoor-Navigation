import pandas as pd
import joblib

from pathlib import Path
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report


BASE_DIR = Path(__file__).resolve().parent

# Load cleaned dataset
df = pd.read_csv(
    BASE_DIR / "dataset" / "processed" /
    "scan_fingerprints_cleaned.csv"
)

# Load Wi-Fi feature columns
feature_columns = joblib.load(
    BASE_DIR / "models" / "feature_columns.pkl"
)

# Identify sessions
df["session"] = (
    df["scan_key"]
    .astype(str)
    .str.extract(r"^(Session\s+\d+)", expand=False)
)

# Prepare features and labels
X = df[feature_columns].fillna(-100)
y = df["location_name"]

# Training: Sessions 1 and 2
train_mask = df["session"].isin(["Session 1", "Session 2"])

# Testing: Sessions 3 and 4
test_mask = df["session"].isin(["Session 3", "Session 4"])

X_train = X.loc[train_mask]
y_train = y.loc[train_mask]

X_test = X.loc[test_mask]
y_test = y.loc[test_mask]


# Define machine learning models
models = {

    "Random Forest": RandomForestClassifier(
        n_estimators=100,
        random_state=42,
        class_weight="balanced"
    ),

    "KNN": make_pipeline(
        StandardScaler(),
        KNeighborsClassifier(
            n_neighbors=3,
            weights="distance"
        )
    ),

    "SVM": make_pipeline(
        StandardScaler(),
        SVC(
            kernel="rbf",
            C=1.0,
            class_weight="balanced"
        )
    )
}


# Compare models
results = []

print("\n========== MODEL COMPARISON ==========")

for name, model in models.items():

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    accuracy = accuracy_score(
        y_test,
        predictions
    )

    results.append((name, accuracy))

    print(f"\nModel: {name}")
    print(f"Accuracy: {accuracy * 100:.2f}%")

    print("\nClassification Report:")

    print(
        classification_report(
            y_test,
            predictions,
            zero_division=0
        )
    )


# Final comparison
print("\n========== FINAL RESULTS ==========")

for name, accuracy in results:

    print(f"{name}: {accuracy * 100:.2f}%")

print("\n===================================")