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

@app.route("/threats", methods=["GET"]) # API endpoint using a Flask GET route that allows users to retrieve a list of known threats, e.g. threat type - DDoS.
def get_threats():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM threats;")
    threats = cursor.fetchall()
    connection.close()
    return jsonify(threats)

@app.route("/threat/<int:id>", methods=["GET"]) # This GET route allows users to fetch the details of a specific threat.
def get_threat(threat_id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM threats WHERE threat_id = %s;", (threat_id,))
    threat = cursor.fetchone()
    connection.close()
    if threat:
        return jsonify(threat)
    return jsonify({"error": "Threat not found."}), 404

@app.route("/report-threat", methods=["POST"]) # POST route allows users to report new threats, logging them in the Threat Intelligence DB.
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

@app.route("/threats", methods=["GET"]) # Implementing an additional GET Flask route that allows users to filter threats based on their type, severity or simply by name.
def get_threats():
    threat_name = request.args.get('threat_name', default=None, type=str)
    threat_type = request.args.get('threat_type', default=None, type=str)
    threat_severity = request.args.get('threat_severity', default=None, type=str)

    query = "SELECT * FROM threats WHERE 1=1"
    params = [ ]

    # Add filters if provided
    if threat_name:
        query += " AND threat_name LIKE %s"
        params.append(f"{threat_name}%")
    if threat_type:
        query += " AND threat_type LIKE %s"
        params.append(threat_type)
    if threat_severity:
        query += " AND threat_severity LIKE %s"
        params.append(threat_severity)

    # Execute the query with filters applied
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(query, tuple(params))
    threats = cursor.fetchall()
    connection.close()

    return jsonify(threats)

if __name__ == "__main__":
    app.run(debug=True)


