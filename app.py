from flask import Flask, request, jsonify
import requests
import re

app = Flask(__name__)

headers = {
    "User-Agent": "Mozilla/5.0"
}

@app.route("/aion2")
def get_character():
    url = request.args.get("url")

    if not url:
        return jsonify({"error": "url required"})

    try:
        res = requests.get(url, headers=headers)

        power_match = re.search(r'"combatPower":([0-9]+)', res.text)
        power = power_match.group(1) if power_match else "0"

        return jsonify({
            "power": power
        })

    except Exception as e:
        return jsonify({"error": str(e)})

app.run(host="0.0.0.0", port=10000)
