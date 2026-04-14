from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

SOLANA_RPC = "https://api.mainnet-beta.solana.com"

ALLOWED_METHODS = {
    "getEpochInfo",
    "getInflationReward",
    "getAccountInfo",
    "getProgramAccounts",
}

def cors_response(data, status=200):
    resp = jsonify(data) if isinstance(data, dict) else app.response_class(response=data, status=status, mimetype="application/json")
    resp.headers["Access-Control-Allow-Origin"] = "*"
    resp.headers["Access-Control-Allow-Methods"] = "POST, OPTIONS"
    resp.headers["Access-Control-Allow-Headers"] = "Content-Type"
    return resp

@app.route("/", methods=["OPTIONS"])
def preflight():
    return cors_response({}), 204

@app.route("/", methods=["POST"])
def proxy():
    try:
        body = request.get_json(force=True)
        method = body.get("method", "")
        if method not in ALLOWED_METHODS:
            return cors_response({"error": f"Method not allowed: {method}"}), 403

        r = requests.post(SOLANA_RPC, json=body, headers={"Content-Type": "application/json"}, timeout=30)
        resp = app.response_class(response=r.text, status=r.status_code, mimetype="application/json")
        resp.headers["Access-Control-Allow-Origin"] = "*"
        return resp
    except Exception as e:
        return cors_response({"error": str(e)}), 500

@app.route("/health", methods=["GET"])
def health():
    resp = jsonify({"status": "ok"})
    resp.headers["Access-Control-Allow-Origin"] = "*"
    return resp

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
