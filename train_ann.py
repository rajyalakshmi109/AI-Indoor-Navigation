import pandas as pd
import numpy as np
import os

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import accuracy_score, classification_report

import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.utils import to_categorical

print("Loading Wi-Fi fingerprints...")

df = pd.read_csv("dataset/processed/scan_fingerprints.csv")

# Features and target
X = df.drop(columns=[
    "scan_key",
    "location_id",
    "location_name",
    "floor"
])

y = df["location_name"]

# Encode location names
encoder = LabelEncoder()
y_encoded = encoder.fit_transform(y)

y_categorical = to_categorical(y_encoded)

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y_categorical,
    test_size=0.2,
    random_state=42,
    stratify=y_encoded
)

# Normalize Wi-Fi features
scaler = StandardScaler()

X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

print("Building ANN model...")

# Artificial Neural Network
model = Sequential([
    Dense(64, activation="relu", input_shape=(X_train.shape[1],)),
    Dropout(0.2),
    Dense(32, activation="relu"),
    Dense(y_categorical.shape[1], activation="softmax")
])

model.compile(
    optimizer="adam",
    loss="categorical_crossentropy",
    metrics=["accuracy"]
)

print("Training ANN...")

model.fit(
    X_train,
    y_train,
    epochs=50,
    batch_size=8,
    validation_split=0.2,
    verbose=1
)

# Evaluate model
loss, accuracy = model.evaluate(X_test, y_test, verbose=0)

print("\nANN Accuracy:", round(accuracy * 100, 2), "%")

# Save model and preprocessing objects
os.makedirs("models", exist_ok=True)

model.save("models/ann_model.keras")

import pickle

with open("models/ann_scaler.pkl", "wb") as f:
    pickle.dump(scaler, f)

with open("models/ann_encoder.pkl", "wb") as f:
    pickle.dump(encoder, f)

print("\nANN model saved successfully!")