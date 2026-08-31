# 🛡️ RiskShield AI

## AI-Powered Transaction Risk Manager

RiskShield AI is a machine-learning-based transaction risk analysis system designed to identify potentially risky transactions and support fraud-risk decision making.

The system analyzes transaction characteristics and assigns a risk score and risk level. Based on the detected risk, it recommends an appropriate action such as approving the transaction, verifying the customer, or sending the transaction for manual review.

---

## 🚀 Features

- Machine-learning-based transaction risk prediction
- Risk percentage calculation
- LOW, MEDIUM and HIGH risk classification
- Recommended actions:
  - APPROVE
  - VERIFY CUSTOMER
  - MANUAL REVIEW
- Explanation of why a transaction was flagged
- Transaction history dashboard
- Batch simulation of 100 transactions
- Risk distribution visualization
- Model performance dashboard
- Confusion matrix evaluation

---

## 🧠 Risk Factors

RiskShield analyzes factors such as:

- Transaction amount
- Failed payment attempts
- Customer account age
- New device usage
- International transaction status

These features are used by the trained model to estimate transaction risk.

---

## 📊 Model Performance

The model was evaluated using a held-out test set from the synthetic transaction dataset.

| Metric | Result |
|---|---:|
| Accuracy | 80.4% |
| Precision | 69.4% |
| Recall | 62.0% |
| F1 Score | 65.49% |

### Confusion Matrix

| | Predicted Safe | Predicted Risk |
|---|---:|---:|
| Actual Safe | 618 | 82 |
| Actual Risk | 114 | 186 |

The prototype uses synthetic transaction data for training and evaluation.

---

## 🧪 Transaction Simulator

RiskShield includes a batch transaction simulator.

The simulator processes 100 generated transactions and summarizes them as:

- Approved
- Verify Customer
- Manual Review

A risk-distribution visualization makes it easy to see how the system responds to a batch of transactions.

A new batch can be generated using the **Run New Simulation** button.

---

## 🛠️ Technologies Used

- Python
- Flask
- Pandas
- NumPy
- Scikit-learn
- HTML
- CSS
- Joblib

---

## 📁 Project Structure

```text
RiskShield-AI/
│
├── data/
│   ├── transactions.csv
│   ├── history.csv
│   └── simulation_results.csv
│
├── model/
│   ├── risk_model.pkl
│   └── metrics.json
│
├── static/
│   └── style.css
│
├── templates/
│   ├── index.html
│   └── simulation.html
│
├── app.py
├── generate_data.py
├── train_model.py
├── simulate_transactions.py
└── README.md
```

---

## ▶️ Running the Project

Install the required Python packages:

```bash
pip install flask pandas numpy scikit-learn joblib
```

Generate the synthetic transaction dataset:

```bash
python generate_data.py
```

Train the machine-learning model:

```bash
python train_model.py
```

Start the Flask application:

```bash
python app.py
```

Then open the local application in your browser.

Main dashboard:

```text
http://127.0.0.1:5000/
```

Transaction simulator:

```text
http://127.0.0.1:5000/simulate
```

---

## ⚠️ Prototype Disclaimer

RiskShield AI is an educational prototype developed using synthetic transaction data. It is not intended to make real financial or payment decisions without further validation, security controls, production data testing, and regulatory review.