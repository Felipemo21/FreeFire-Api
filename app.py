from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route("/api/v1/account")
def get_account():
    uid = request.args.get("uid")
    region = request.args.get("region", "SG")

    if not uid:
        return jsonify({"error": "UID requerido"}), 400

    try:
        url = f"https://account-info.ff.garena.com/?uid={uid}&region={region}"
        headers = {
            "User-Agent": "Mozilla/5.0"
        }
        res = requests.get(url, headers=headers, timeout=10)
        data = res.json()

        if "nickname" in data.get("basicInfo", {}):
            return jsonify({
                "uid": uid,
                "region": region,
                "nickname": data["basicInfo"]["nickname"]
            })
        else:
            return jsonify({"error": "Jugador no encontrado"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
