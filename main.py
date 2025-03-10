from db_utils import get_db_connection

conn = get_db_connection()
if conn:
    print("Connected to MySQL successfully!")
    conn.close()
else:
    print("Failed to connect to MySQL.")

from flask import Flask, jsonify, request
from db_utils import get_db_connection

app = Flask(__name__)

@app.route("/threats", methods=["GET"])
def get_threats():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM threats;")
    threats = cursor.fetchall()
    connection.close()
    return jsonify(threats)

@app.route("/threat/<int:id>", methods=["GET"])
def get_threat(id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM threats WHERE id = %s;", (id,))
    threat = cursor.fetchone()
    connection.close()
    if threat:
        return jsonify(threat)
    return jsonify({"error": "Threat not found."}), 404

@app.route("/report-threat", methods=["POST"])
def report_threat():
    data = request.get_json()
    threat_name = data.get("threat_name")
    threat_description = data.get("threat_description")
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO threats (threat_name, threat_description) VALUES (%s, %s);",
        (threat_name, threat_description)
    )
    connection.commit()
    connection.close()
    return jsonify({"message": "Threat reported successfully"}), 201

if __name__ == "__main__":
    app.run(debug=True)

