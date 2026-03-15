from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # allow UI to call API locally

bugs = []
next_id = 1

def find_bug(bug_id: int):
    return next((b for b in bugs if b["id"] == bug_id), None)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/bugs")
def list_bugs():
    return jsonify(bugs)

@app.post("/bugs")
def create_bug():
    global next_id
    data = request.get_json(force=True) or {}

    title = (data.get("title") or "").strip()
    severity = (data.get("severity") or "").strip()
    status = (data.get("status") or "Open").strip()

    if not title:
        return jsonify({"error": "Bug title is required."}), 400
    if severity not in {"Low", "Medium", "High", "Critical"}:
        return jsonify({"error": "Severity must be one of Low/Medium/High/Critical."}), 400
    if status not in {"Open", "In Progress", "Closed"}:
        return jsonify({"error": "Status must be Open/In Progress/Closed."}), 400

    bug = {"id": next_id, "title": title, "severity": severity, "status": status}
    next_id += 1
    bugs.append(bug)
    return jsonify(bug), 201

@app.put("/bugs/<int:bug_id>")
def update_bug(bug_id: int):
    bug = find_bug(bug_id)
    if not bug:
        return jsonify({"error": "Bug not found."}), 404

    data = request.get_json(force=True) or {}

    if "title" in data:
        title = (data.get("title") or "").strip()
        if not title:
            return jsonify({"error": "Bug title is required."}), 400
        bug["title"] = title

    if "severity" in data:
        severity = (data.get("severity") or "").strip()
        if severity not in {"Low", "Medium", "High", "Critical"}:
            return jsonify({"error": "Severity must be one of Low/Medium/High/Critical."}), 400
        bug["severity"] = severity

    if "status" in data:
        status = (data.get("status") or "").strip()
        if status not in {"Open", "In Progress", "Closed"}:
            return jsonify({"error": "Status must be Open/In Progress/Closed."}), 400
        bug["status"] = status

    return jsonify(bug)

@app.delete("/bugs/<int:bug_id>")
def delete_bug(bug_id: int):
    bug = find_bug(bug_id)
    if not bug:
        return jsonify({"error": "Bug not found."}), 404

    bugs.remove(bug)
    return "", 204

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)