from flask import Flask, jsonify
import requests
import os

app = Flask(__name__)
DATABASE_URL = os.environ.get("DATABASE_URL", "http://database-service:5002")

@app.route("/")
def home():
    return jsonify({"service": "backend", "status": "ok"})

@app.route("/process")
def process():
    try:
        response = requests.get(f"{DATABASE_URL}/query", timeout=5)
        return jsonify({"backend": "ok", "data": response.json()})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)