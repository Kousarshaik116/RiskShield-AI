from flask import Flask, render_template, request
import joblib
import pandas as pd
import os
import json
from datetime import datetime
from simulate_transactions import run_simulation

app = Flask(__name__)

# Load trained AI model
model = joblib.load("model/risk_model.pkl")


@app.route("/", methods=["GET", "POST"])
def home():

    result = None
    history_file = "data/history.csv"

    # -----------------------------
    # ANALYZE ONE TRANSACTION
    # -----------------------------
    if request.method == "POST":

        amount = float(request.form["amount"])
        failed_attempts = int(request.form["failed_attempts"])
        new_device = int(request.form["new_device"])
        account_age_days = int(request.form["account_age_days"])
        international = int(request.form["international"])

        transaction = pd.DataFrame([{
            "amount": amount,
            "failed_attempts": failed_attempts,
            "new_device": new_device,
            "account_age_days": account_age_days,
            "international": international
        }])

        risk_probability = model.predict_proba(transaction)[0][1]
        risk_percent = round(risk_probability * 100, 2)

        # -----------------------------
        # EXPLANATION SIGNALS
        # -----------------------------
        reasons = []

        if amount > 50000:
            reasons.append("Unusually high transaction amount")

        if failed_attempts >= 5:
            reasons.append("Multiple failed payment attempts")

        if new_device == 1:
            reasons.append("Transaction initiated from a new device")

        if account_age_days < 30:
            reasons.append("Very new customer account")

        if international == 1:
            reasons.append("International transaction")

        if not reasons:
            reasons.append("No major risk signals detected")

        # -----------------------------
        # RISK LEVEL + ACTION
        # -----------------------------
        if risk_percent < 30:
            risk_level = "LOW"
            action = "APPROVE"

        elif risk_percent < 70:
            risk_level = "MEDIUM"
            action = "VERIFY CUSTOMER"

        else:
            risk_level = "HIGH"
            action = "MANUAL REVIEW"

        result = {
            "risk_percent": risk_percent,
            "risk_level": risk_level,
            "action": action,
            "reasons": reasons
        }

        # -----------------------------
        # SAVE TRANSACTION HISTORY
        # -----------------------------
        history_row = pd.DataFrame([{
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "amount": amount,
            "failed_attempts": failed_attempts,
            "account_age_days": account_age_days,
            "new_device": new_device,
            "international": international,
            "risk_percent": risk_percent,
            "risk_level": risk_level,
            "action": action
        }])

        if os.path.exists(history_file) and os.path.getsize(history_file) > 0:

            history_row.to_csv(
                history_file,
                mode="a",
                header=False,
                index=False
            )

        else:

            history_row.to_csv(
                history_file,
                index=False
            )

    # -----------------------------
    # DASHBOARD TRANSACTION STATS
    # -----------------------------
    history = []

    stats = {
        "total": 0,
        "approved": 0,
        "high_risk": 0,
        "manual_review": 0
    }

    if os.path.exists(history_file) and os.path.getsize(history_file) > 0:

        history_data = pd.read_csv(history_file)

        stats["total"] = len(history_data)

        stats["approved"] = (
            history_data["action"] == "APPROVE"
        ).sum()

        stats["high_risk"] = (
            history_data["risk_level"] == "HIGH"
        ).sum()

        stats["manual_review"] = (
            history_data["action"] == "MANUAL REVIEW"
        ).sum()

        history = (
            history_data
            .tail(10)
            .iloc[::-1]
            .to_dict(orient="records")
        )

    # -----------------------------
    # LOAD MODEL PERFORMANCE
    # -----------------------------
    metrics = {
        "accuracy": 0,
        "precision": 0,
        "recall": 0,
        "f1": 0,
        "true_negative": 0,
        "false_positive": 0,
        "false_negative": 0,
        "true_positive": 0
    }

    metrics_file = "model/metrics.json"

    if os.path.exists(metrics_file):

        with open(metrics_file, "r") as file:
            metrics = json.load(file)

    # -----------------------------
    # SEND EVERYTHING TO DASHBOARD
    # -----------------------------
    return render_template(
        "index.html",
        result=result,
        history=history,
        stats=stats,
        metrics=metrics
    )


# -----------------------------
# SIMULATOR PAGE
# -----------------------------
@app.route("/simulate", methods=["GET", "POST"])
def simulate():

    simulation_file = "data/simulation_results.csv"

    simulation_stats = {
        "total": 0,
        "approved": 0,
        "verify": 0,
        "manual_review": 0
    }

    if request.method == "POST":

        simulation_stats = run_simulation()

    else:

        if os.path.exists(simulation_file):

            simulation_data = pd.read_csv(simulation_file)

            simulation_stats["total"] = len(simulation_data)

            simulation_stats["approved"] = (
                simulation_data["action"] == "APPROVE"
            ).sum()

            simulation_stats["verify"] = (
                simulation_data["action"] == "VERIFY CUSTOMER"
            ).sum()

            simulation_stats["manual_review"] = (
                simulation_data["action"] == "MANUAL REVIEW"
            ).sum()

    return render_template(
        "simulation.html",
        simulation_stats=simulation_stats
    )


if __name__ == "__main__":
    app.run(debug=True)