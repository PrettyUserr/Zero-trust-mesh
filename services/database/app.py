from flask import Flask, jsonify

app = Flask(__name__)

MOCK_DATA = [
    {"id": 1, "record": "patient_001", "value": "sensitive_data_A"},
    {"id": 2, "record": "patient_002", "value": "sensitive_data_B"},
    {"id": 3, "record": "patient_003", "value": "sensitive_data_C"},
]

@app.route("/")
def home():
    return jsonify({"service": "database", "status": "ok"})

@app.route("/query")
def query():
    return jsonify({"database": "ok", "records": MOCK_DATA})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)