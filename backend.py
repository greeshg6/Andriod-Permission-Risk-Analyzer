import gzip
import json
import os
from flask import Flask, render_template, request, jsonify
from risk import calculate_risk

app = Flask(__name__)

json_path = os.path.join(app.root_path, "apps.json")
gzip_path = json_path + ".gz"

if os.path.exists(gzip_path):
    data_path = gzip_path
    open_func = lambda path: gzip.open(path, "rt", encoding="utf-8")
elif os.path.exists(json_path):
    data_path = json_path
    open_func = lambda path: open(path, "r", encoding="utf-8")
else:
    raise FileNotFoundError("Missing dataset. Place apps.json or apps.json.gz in the app root.")


def _stream_app_objects():
    """Yield app objects from the JSON array without loading the full file."""

    with open_func(data_path) as f:
        in_string = False
        escape = False
        depth = 0
        buffer = ""
        started = False

        while True:
            chunk = f.read(65536)
            if not chunk:
                break

            for ch in chunk:
                if not started:
                    if ch.isspace():
                        continue
                    if ch == "[":
                        started = True
                        continue
                    raise ValueError("Dataset must start with a JSON array")

                if depth == 0 and ch in ", \n\r\t":
                    continue
                if depth == 0 and ch == "]":
                    return

                buffer += ch

                if ch == "\\" and not escape:
                    escape = True
                    continue
                if ch == '"' and not escape:
                    in_string = not in_string
                escape = False

                if not in_string:
                    if ch == "{":
                        depth += 1
                    elif ch == "}":
                        depth -= 1
                        if depth == 0:
                            yield json.loads(buffer)
                            buffer = ""

        if buffer.strip():
            raise ValueError("Incomplete JSON object in dataset")


def _find_app(app_name_lower):
    for app_data in _stream_app_objects():
        if app_name_lower in app_data["appName"].lower():
            return app_data
    return None

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/search", methods=["POST"])
def search():

    data = request.get_json()

    app_name = data["app_name"].lower()
    app_data = _find_app(app_name)

    if not app_data:
        return jsonify({
            "found": False
        })

    permissions = app_data["allPermissions"]
    permission_types = [p["type"] for p in permissions]

    score, level, breakdown, explanation, recommendations = calculate_risk(
        permission_types
    )

    return jsonify({
        "found": True,
        "appName": app_data["appName"],
        "appId": app_data["appId"],
        "permissions": permissions,
        "riskScore": score,
        "riskLevel": level,
        "riskBreakdown": breakdown,
        "explanation": explanation,
        "recommendations": recommendations
    })

if __name__ == "__main__":
    app.run(debug=True)