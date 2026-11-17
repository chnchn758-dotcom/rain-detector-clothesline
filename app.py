from flask import Flask, request, jsonify, render_template
import mysql.connector

app = Flask(__name__)

DB_CONFIG = {
    "host": "127.0.0.1",
    "port": 3307,
    "user": "rain_user",
    "password": "change_this_password",
    "database": "rain_dashboard",
}


def get_db():
    return mysql.connector.connect(**DB_CONFIG)


@app.route("/")
def dashboard():
    return render_template("index.html")


@app.route("/api/rain", methods=["POST"])
def add_event():
    data = request.get_json(silent=True) or {}
    status = data.get("status")

    if status not in ("rain", "dry"):
        return jsonify({"error": "status must be 'rain' or 'dry'"}), 400

    db = get_db()
    cur = db.cursor()
    cur.execute("INSERT INTO rain_events (status) VALUES (%s)", (status,))
    db.commit()
    event_id = cur.lastrowid
    cur.close()
    db.close()

    return jsonify({"ok": True, "id": event_id}), 201


@app.route("/api/events")
def list_events():
    limit = min(request.args.get("limit", 50, type=int), 500)

    db = get_db()
    cur = db.cursor(dictionary=True)
    cur.execute(
        "SELECT id, status, created_at FROM rain_events ORDER BY id DESC LIMIT %s",
        (limit,),
    )
    rows = cur.fetchall()
    cur.close()
    db.close()

    for row in rows:
        row["created_at"] = row["created_at"].strftime("%Y-%m-%d %H:%M:%S")

    return jsonify(rows)


@app.route("/api/status")
def current_status():
    db = get_db()
    cur = db.cursor(dictionary=True)
    cur.execute("SELECT status, created_at FROM rain_events ORDER BY id DESC LIMIT 1")
    row = cur.fetchone()
    cur.close()
    db.close()

    if row is None:
        return jsonify({"status": "unknown", "since": None})

    return jsonify({
        "status": row["status"],
        "since": row["created_at"].strftime("%Y-%m-%d %H:%M:%S"),
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)