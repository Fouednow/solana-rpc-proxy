from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

SOLANA_RPC = "https://api.mainnet-beta.solana.com"

ALLOWED_METHODS = {
    "getEpochInfo",
    "getInflationReward",
    "getAccountInfo",
    "getProgramAccounts",
}

@app.route("/", methods=["POST"])
def proxy():
    try:
        body = request.get_json(force=True)
        method = body.get("method", "")
        if method not in ALLOWED_METHODS:
            return jsonify({"error": f"Method not allowed: {method}"}), 403

        r = requests.post(SOLANA_RPC, json=body, headers={"Content-Type": "application/json"}, timeout=60)
        resp = make_response(r.text, r.status_code)
        resp.headers["Content-Type"] = "application/json"
        return resp
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
