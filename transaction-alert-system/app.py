from flask import Flask, jsonify, request, Response
import pandas as pd
from datetime import datetime, timedelta
import numpy as np
import time
import threading

app = Flask(__name__)

# Load CSV data
transactions = pd.read_csv("transactions.csv")
auth_codes = pd.read_csv("transactions_auth_codes.csv")

# Historical logs
transaction_history = []
alert_history = []

# Thresholds for triggering alerts
ALERT_THRESHOLDS = {
    'failed': 0.1,
    'reversed': 0.05,
    'denied': 0.08
}

def send_alert(message):
    print(f"ALERT: {message}")
    alert_history.append({
        'timestamp': datetime.now().isoformat(),
        'message': message
    })

def analyze_anomalies(data):
    total = len(data)
    if total == 0:
        return {"status": "no data", "percentages": {}, "recommendation": "no action"}

    counts = data['status'].value_counts().to_dict()
    percentages = {k: v / total for k, v in counts.items()}

    alerts = []
    for status, threshold in ALERT_THRESHOLDS.items():
        if status in percentages and percentages[status] > threshold:
            alerts.append(f"{status.capitalize()} transactions above normal: {percentages[status]*100:.2f}%")

    if alerts:
        recommendation = "alert"
        for alert in alerts:
            send_alert(alert)
    else:
        recommendation = "ok"

    return {
        "status": "analyzed",
        "transaction_count": total,
        "percentages": percentages,
        "recommendation": recommendation,
        "alerts": alerts if alerts else ["No anomalies detected"]
    }

@app.route("/")
def home():
    return jsonify({"status": "Monitoring API is running"})

@app.route("/transactions")
def get_transactions():
    return jsonify(transactions.to_dict(orient="records"))

@app.route("/auth_codes")
def get_auth_codes():
    return jsonify(auth_codes.to_dict(orient="records"))

@app.route("/summary")
def get_summary():
    grouped = transactions.groupby("status").size().reset_index(name="count")
    return jsonify(grouped.to_dict(orient="records"))

@app.route("/analyze", methods=['GET', 'POST'])
def analyze():
    if request.method == 'POST':
        new_data = request.json
        new_df = pd.DataFrame(new_data)
        result = analyze_anomalies(new_df)
        transaction_history.append({
            'timestamp': datetime.now().isoformat(),
            'data': new_df.to_dict(orient='records'),
            'analysis': result
        })
        return jsonify(result)
    else:
        result = analyze_anomalies(transactions)
        return jsonify(result)

@app.route("/metrics")
def metrics():
    try:
        grouped = transactions.groupby("status").size()
        metrics_data = {
            "status": "success",
            "data": {
                "counts": grouped.to_dict(),
                "percentages": analyze_anomalies(transactions).get('percentages', {})
            },
            "timestamps": {
                "last_update": datetime.now().isoformat()
            }
        }
        return jsonify(metrics_data)

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e),
            "timestamp": datetime.now().isoformat()
        }), 500

@app.route("/alerts")
def get_alerts():
    return jsonify(alert_history)

# Status endpoints (plain number only)
@app.route("/approved")
def get_approved():
    count = transactions[transactions["status"].str.lower() == "approved"].shape[0]
    return Response(str(count), mimetype='text/plain')

@app.route("/denied")
def get_denied():
    count = transactions[transactions["status"].str.lower() == "denied"].shape[0]
    return Response(str(count), mimetype='text/plain')

@app.route("/failed")
def get_failed():
    count = transactions[transactions["status"].str.lower() == "failed"].shape[0]
    return Response(str(count), mimetype='text/plain')

@app.route("/reversed")
def get_reversed():
    count = transactions[transactions["status"].str.lower() == "reversed"].shape[0]
    return Response(str(count), mimetype='text/plain')

@app.route("/backend_reversed")
def get_backend_reversed():
    count = transactions[transactions["status"].str.lower() == "backend_reversed"].shape[0]
    return Response(str(count), mimetype='text/plain')

@app.route("/refunded")
def get_refunded():
    count = transactions[transactions["status"].str.lower() == "refunded"].shape[0]
    return Response(str(count), mimetype='text/plain')

# Optional: simulate incoming transactions
def simulate_realtime_transactions():
    while True:
        time.sleep(60)
        new_transactions = pd.DataFrame([{
            'id': np.random.randint(10000, 99999),
            'status': np.random.choice(
                ['approved', 'failed', 'reversed', 'denied', 'refunded', 'backend_reversed'],
                p=[0.8, 0.05, 0.05, 0.05, 0.025, 0.025]
            ),
            'amount': np.random.uniform(10, 1000),
            'timestamp': datetime.now().isoformat()
        } for _ in range(np.random.randint(5, 20))])

        transaction_history.append({
            'timestamp': datetime.now().isoformat(),
            'data': new_transactions.to_dict(orient='records')
        })
        analyze_anomalies(new_transactions)

if __name__ == "__main__":
    if not app.config.get('TESTING'):
        thread = threading.Thread(target=simulate_realtime_transactions)
        thread.daemon = True
        thread.start()

    app.run(debug=True, host="0.0.0.0", port=5000)
