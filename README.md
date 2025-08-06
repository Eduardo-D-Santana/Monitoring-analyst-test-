<img width="1671" height="993" alt="image" src="https://github.com/user-attachments/assets/fcf4c350-5a80-4bf9-952f-358389197bf9" />

# Transaction Anomaly Alert System

This project is a solution to the technical challenge of creating a monitoring system with transaction anomaly alerts, using historical data and simple rule-based logic.

## 🔧 Technologies

- Python 3
- Flask
- Pandas
- Grafana (for visualization)
- CSV as a data source

## 📁 Structure

- `app.py`: API with endpoints for accessing data, summarizing status, and issuing alerts.
- `data/`: Contains the `transactions.csv` and `transactions_auth_codes.csv` files.
- `dashboards/`: Structure for exporting Grafana dashboards.
- `report.pdf`: Technical report explaining logic, architecture, and decisions.

## 📊 Endpoints

- `/`: API health test.
- `/transactions`: Complete list of transactions.
- `/auth_codes`: Complete list of authorization codes.
- `/summary`: Returns the total by transaction status.
- `/alert`: Detects anomalies in the last 5 minutes based on the historical average.

## 🚨 Alert Logic

Uses a rule-based model:
- If the number of `FAILED`, `REVERSED`, `DENIED`, `BACKEND_REVERSED`, or `REFUNDED` transactions in the last 5 minutes is 50% higher than the historical average per minute, an alert is issued.

## ▶️ How to run

```bash
# Install the dependencies
pip install -r requirements.txt

# Run the API
python3 app.py
