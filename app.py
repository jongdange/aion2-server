from flask import Flask, request, jsonify
import requests
import re

app = Flask(__name__)

headers = {
    "User-Agent": "Mozilla/5.0"
}

@app.route("/aion2")
def get_character():
    name = request.args.get("name")

    if not name:
        return jsonify({"error": "name required"})

    try:
        search_url = f"https://aion2.plaync.com/search?query={name}"
        res = requests.get(search_url, headers=headers)

        match = re.search(r'/ko-kr/characters/[0-9]+/[A-Za-z0-9\-_=%]+', res.text)
        if not match:
            return jsonify({"error": "not found"})

        char_url = "https://aion2.plaync.com" + match.group()
        res2 = requests.get(char_url, headers=headers)

        power_match = re.search(r'"combatPower":([0-9]+)', res2.text)
        power = power_match.group(1) if power_match else "0"

        return jsonify({"name": name, "power": power})

    except Exception as e:
        return jsonify({"error": str(e)})

app.run(host="0.0.0.0", port=10000)