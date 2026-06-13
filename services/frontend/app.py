from flask import Flask, jsonify
import requests
import os

app = Flask(__name__)
BACKEND_URL = os.environ.get("BACKEND_URL", "http://backend-service:5001")

@app.route("/")
def home():
    return jsonify({"service": "frontend", "status": "ok"})

@app.route("/data")
def get_data():
    try:
        response = requests.get(f"{BACKEND_URL}/process", timeout=5)
        return jsonify({"frontend": "ok", "backend_response": response.json()})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)