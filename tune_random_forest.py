import pandas as pd
import joblib

from pathlib import Path

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV, StratifiedKFold
from sklearn.metrics import accuracy_score, classification_report, f1_score


BASE_DIR = Path(__file__).resolve().parent

# Load cleaned dataset
df = pd.read_csv(
    BASE_DIR / "dataset" / "processed" /
    "scan_fingerprints_cleaned.csv"
)

# Load feature columns
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


# Baseline Random Forest
baseline = RandomForestClassifier(
    n_estimators=100,
    random_state=42,
    class_weight="balanced",
    n_jobs=1
)

baseline.fit(X_train, y_train)

baseline_predictions = baseline.predict(X_test)

baseline_accuracy = accuracy_score(
    y_test,
    baseline_predictions
)


# Hyperparameter combinations
param_grid = {

    "n_estimators": [100, 200],

    "max_depth": [None, 10],

    "min_samples_split": [2, 4],

    "min_samples_leaf": [1, 2],

    "max_features": ["sqrt", 0.5]
}


# Cross-validation
cv = StratifiedKFold(
    n_splits=3,
    shuffle=True,
    random_state=42
)


# Grid Search
grid_search = GridSearchCV(
    estimator=RandomForestClassifier(
        random_state=42,
        class_weight="balanced",
        n_jobs=1
    ),

    param_grid=param_grid,

    scoring="f1_macro",

    cv=cv,

    n_jobs=1,

    refit=True
)


print("\n========== RANDOM FOREST TUNING ==========")

print("\nTraining model configurations...")

grid_search.fit(X_train, y_train)


# Best model
best_model = grid_search.best_estimator_

tuned_predictions = best_model.predict(X_test)

tuned_accuracy = accuracy_score(
    y_test,
    tuned_predictions
)

tuned_f1 = f1_score(
    y_test,
    tuned_predictions,
    average="macro"
)


# Display results
print("\nBest Parameters:")

print(grid_search.best_params_)

print(
    f"\nBest Cross-Validation Macro F1: "
    f"{grid_search.best_score_ * 100:.2f}%"
)

print("\n========== ACCURACY COMPARISON ==========")

print(
    f"Baseline Random Forest: "
    f"{baseline_accuracy * 100:.2f}%"
)

print(
    f"Tuned Random Forest: "
    f"{tuned_accuracy * 100:.2f}%"
)

print(
    f"Tuned Test Macro F1: "
    f"{tuned_f1 * 100:.2f}%"
)

print("\nTuned Model Classification Report:")

print(
    classification_report(
        y_test,
        tuned_predictions,
        zero_division=0
    )
)

print("\n=========================================")
