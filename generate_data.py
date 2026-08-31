import pandas as pd
import numpy as np
import os

# Make the random data repeatable
np.random.seed(42)

# Number of transactions we want to create
number_of_transactions = 5000

# Create fake transaction information
amount = np.random.randint(100, 100000, number_of_transactions)
failed_attempts = np.random.randint(0, 10, number_of_transactions)
new_device = np.random.randint(0, 2, number_of_transactions)
account_age_days = np.random.randint(1, 1000, number_of_transactions)
international = np.random.randint(0, 2, number_of_transactions)

# Start every transaction with a risk score of 0
risk_score = np.zeros(number_of_transactions)

# Add risk points for suspicious behaviour
risk_score += (amount > 50000) * 2
risk_score += (failed_attempts >= 5) * 3
risk_score += (new_device == 1) * 1
risk_score += (account_age_days < 30) * 2
risk_score += (international == 1) * 1

# Add a little randomness so the dataset isn't perfectly predictable
risk_score += np.random.normal(0, 1.5, number_of_transactions)

# Transactions with a high enough score are labelled risky
is_fraud = (risk_score >= 5).astype(int)

# Put everything into a table
data = pd.DataFrame({
    "amount": amount,
    "failed_attempts": failed_attempts,
    "new_device": new_device,
    "account_age_days": account_age_days,
    "international": international,
    "is_fraud": is_fraud
})

# Make sure the data folder exists
os.makedirs("data", exist_ok=True)

# Save the table as a CSV file
data.to_csv("data/transactions.csv", index=False)

print("Dataset created successfully!")
print("Total transactions:", len(data))
print("Normal transactions:", (data["is_fraud"] == 0).sum())
print("Risky transactions:", (data["is_fraud"] == 1).sum())

print("\nFirst 5 transactions:")
print(data.head())