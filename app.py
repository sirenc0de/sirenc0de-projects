from flask import Flask, jsonify, request
from db_utils import get_db_connection # Import database connection function

# Initialise the Flask application
app = Flask(__name__)

# API Endpoint 1: Retrieve a list of all known threats (with optional filters).
@app.route("/threats", methods=["GET"])
def get_threats():
    connection = None  # to ensure connection is defined even if an exception occurs early
    cursor = None
    """
    Fetch all threats from the database. Optional filters: threat_name, threat_type, threat_severity.
    """
    threat_name = request.args.get("threat_name")
    threat_type = request.args.get("threat_type")
    threat_severity = request.args.get("threat_severity")

    query = "SELECT * FROM threats WHERE 1=1"
    params = [ ]

    if threat_name:
        query += " AND threat_name LIKE %s"
        params.append(f"{threat_name}%")
    if threat_type:
        query += " AND threat_type LIKE %s"
        params.append(threat_type)
    if threat_severity:
        query += " AND threat_severity LIKE %s"
        params.append(threat_severity)

    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute(query, tuple(params))
        threats = cursor.fetchall()
        return jsonify(threats)

    except Exception as e:
        return jsonify({"error": str(e)}), 500 # Handle errors

    finally:
        cursor.close()
        connection.close()

# API Endpoint 2: Fetch the details of a specific threat.
@app.route("/threat/<int:threat_id>", methods=["GET"])
def get_threat(threat_id):
    connection = None
    cursor = None
    """
    Fetch a specific threat using its ID.
    """
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM threats WHERE threat_id = %s;", (threat_id,))
        threat = cursor.fetchone()

        if not threat:
            return jsonify({"error": "Threat not found."}), 404
        return jsonify(threat)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        cursor.close()
        connection.close()

# API Endpoint 3: Report a new threat.
@app.route("/report-threat", methods=["POST"])
def report_threat():
    connection = None
    cursor = None
    """
    Allow users to report a new threat.
    Requires: threat_name, threat_description.
    """
    # Get the threat intelligence data from the request body in JSON format.
    data = request.get_json()
    threat_name = data.get("threat_name")
    threat_description = data.get("threat_description")

    if not threat_name or not threat_description:
        return jsonify({"error": "Missing required fields."}), 400

    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO threats (threat_name, threat_description) VALUES (%s, %s);",
            (threat_name, threat_description)
        )
        connection.commit()
        return jsonify({"message": "Threat reported successfully!"}), 201

    except Exception as e:
        return jsonify({"message": str(e)}), 500

    finally:
        cursor.close()
        connection.close()

# API Endpoint 4: Update an existing threat.
@app.route("/threats/<int:threat_id>", methods=["PUT"])
def update_threat(threat_id):
    connection = None
    cursor = None
    """
    Update an existing threat in the database.
    Requires: threat_name, threat_type, threat_severity, threat_description.
    """
    data = request.get_json()
    threat_name = data.get("threat_name")
    threat_type = data.get("threat_type")
    threat_severity = data.get("threat_severity")
    threat_description = data.get("threat_description")

    if not all([threat_name, threat_type, threat_severity, threat_description]):
        return jsonify({"error": "Missing required fields!"}), 400

    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        # Check if the threat exists
        cursor.execute("SELECT * FROM threats WHERE threat_id = %s", (threat_id,))
        cursor.fetchall() # Fetch and discard the result to clear the cursor's buffer

        # Update relevant threat
        cursor.execute("""
            UPDATE threats
            SET threat_name = %s, threat_type = %s, threat_severity = %s, threat_description = %s
            WHERE threat_id = %s
        """, (threat_name, threat_type, threat_severity, threat_description, threat_id))

        connection.commit()
        return jsonify({"message": "Threat updated successfully!"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        cursor.close()
        connection.close()

