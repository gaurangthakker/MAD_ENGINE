from flask import Flask, jsonify
import os
import json
import requests
from flask_cors import CORS

app = Flask(__name__)

CORS(app)

REST_URL = os.environ.get("UPSTASH_REDIS_REST_URL")
REST_TOKEN = os.environ.get("UPSTASH_REDIS_REST_TOKEN")


@app.route("/")
def home():
    return {
        "status": "OK",
        "app": "MAD ENGINE",
        "version": "2.0"
    }


@app.route("/api/live")
def api_live():

    if not REST_URL or not REST_TOKEN:
        return jsonify({
            "error": "Redis Environment Variables Missing"
        }), 500

    headers = {
        "Authorization": f"Bearer {REST_TOKEN}"
    }

    try:

        response = requests.get(
            f"{REST_URL}/get/live_status",
            headers=headers,
            timeout=5,
        )

        response.raise_for_status()

        result = response.json()

        if result.get("result") is None:
            return jsonify({})

        return jsonify(json.loads(result["result"]))

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True,
    )