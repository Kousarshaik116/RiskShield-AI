import pandas as pd
import joblib
import os
import json

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix
)

# Load dataset
data = pd.read_csv("data/transactions.csv")

# Input features
X = data[
    [
        "amount",
        "failed_attempts",
        "new_device",
        "account_age_days",
        "international"
    ]
]

# Target
y = data["is_fraud"]

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

# Create model
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

# Train model
model.fit(X_train, y_train)

# Predict on test data
predictions = model.predict(X_test)

# Calculate metrics
accuracy = accuracy_score(y_test, predictions)
precision = precision_score(y_test, predictions)
recall = recall_score(y_test, predictions)
f1 = f1_score(y_test, predictions)

matrix = confusion_matrix(
    y_test,
    predictions
)

# Print results
print("Model training completed!")
print()

print("Accuracy:", round(accuracy, 4))
print("Precision:", round(precision, 4))
print("Recall:", round(recall, 4))
print("F1 Score:", round(f1, 4))

print()
print("Confusion Matrix:")
print(matrix)

# Create model folder
os.makedirs(
    "model",
    exist_ok=True
)

# Save trained model
joblib.dump(
    model,
    "model/risk_model.pkl"
)

# Save metrics
metrics = {
    "accuracy": round(accuracy * 100, 2),
    "precision": round(precision * 100, 2),
    "recall": round(recall * 100, 2),
    "f1": round(f1 * 100, 2),
    "true_negative": int(matrix[0][0]),
    "false_positive": int(matrix[0][1]),
    "false_negative": int(matrix[1][0]),
    "true_positive": int(matrix[1][1])
}

with open(
    "model/metrics.json",
    "w"
) as file:

    json.dump(
        metrics,
        file,
        indent=4
    )

print()
print("Model saved successfully!")
print("Saved at: model/risk_model.pkl")

print()
print("Metrics saved successfully!")
print("Saved at: model/metrics.json")