import pandas as pd
import numpy as np
import joblib


def run_simulation(number_of_transactions=100):

    # Load trained model
    model = joblib.load("model/risk_model.pkl")

    # Create random transactions
    amount = np.random.randint(
        100,
        100000,
        number_of_transactions
    )

    failed_attempts = np.random.randint(
        0,
        10,
        number_of_transactions
    )

    new_device = np.random.randint(
        0,
        2,
        number_of_transactions
    )

    account_age_days = np.random.randint(
        1,
        1000,
        number_of_transactions
    )

    international = np.random.randint(
        0,
        2,
        number_of_transactions
    )

    transactions = pd.DataFrame({
        "amount": amount,
        "failed_attempts": failed_attempts,
        "new_device": new_device,
        "account_age_days": account_age_days,
        "international": international
    })

    # Get risk probabilities
    risk_probabilities = model.predict_proba(
        transactions
    )[:, 1]

    transactions["risk_percent"] = np.round(
        risk_probabilities * 100,
        2
    )

    # Decide risk level
    def get_risk_level(score):

        if score < 30:
            return "LOW"

        elif score < 70:
            return "MEDIUM"

        else:
            return "HIGH"

    transactions["risk_level"] = transactions[
        "risk_percent"
    ].apply(get_risk_level)

    # Decide action
    def get_action(level):

        if level == "LOW":
            return "APPROVE"

        elif level == "MEDIUM":
            return "VERIFY CUSTOMER"

        else:
            return "MANUAL REVIEW"

    transactions["action"] = transactions[
        "risk_level"
    ].apply(get_action)

    # Count results
    approved = (
        transactions["action"] == "APPROVE"
    ).sum()

    verify = (
        transactions["action"] == "VERIFY CUSTOMER"
    ).sum()

    manual_review = (
        transactions["action"] == "MANUAL REVIEW"
    ).sum()

    # Save results
    transactions.to_csv(
        "data/simulation_results.csv",
        index=False
    )

    # Send results back to Flask
    return {
        "total": number_of_transactions,
        "approved": int(approved),
        "verify": int(verify),
        "manual_review": int(manual_review)
    }


# This part lets us still run the file manually
if __name__ == "__main__":

    results = run_simulation()

    print("RiskShield AI Transaction Simulator")
    print("----------------------------------")

    print("Transactions processed:", results["total"])
    print("Approved:", results["approved"])
    print("Verification required:", results["verify"])
    print("Manual review:", results["manual_review"])

    print()
    print("Simulation complete!")
    print("Results saved to data/simulation_results.csv")