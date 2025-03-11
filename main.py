# Import necessary modules from Flask, MySQL connector
from flask import Flask, jsonify, request
from db_utils import get_db_connection # Import database connection function

# Initialise the Flask application
app = Flask(__name__)

# API Endpoint: Retrieve a list of known threats (with optional filters).
@app.route("/threats", methods=["GET"])
def get_threats():
    """
    Fetch all threats from the database. Optional filters: threat_name, threat_type, threat_severity.
    """
    threat_name = request.args.get('threat_name')
    threat_type = request.args.get('threat_type')
    threat_severity = request.args.get('threat_severity')

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

# API Endpoint: Fetch the details of a specific threat.
@app.route("/threat/<int:threat_id>", methods=["GET"])
def get_threat(threat_id):
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

# POST route allows users to report new threats, logging them in the Threat Intelligence DB.
@app.route("/report-threat", methods=["POST"])
def report_threat():
    # Get the threat intelligence data from the request body in JSON format.
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

# GET route that allows users to filter threats based on their type, severity or simply by name.
@app.route("/threats", methods=["GET"])
def get_threats(): # Extract required values from the request
    threat_name = request.args.get('threat_name', default=None)
    threat_type = request.args.get('threat_type', default=None)
    threat_severity = request.args.get('threat_severity', default=None)

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

#
@app.route("/threats/<int:threat_id>", methods=["PUT"])
def update_threat(threat_id):
    connection = None # Initialise connection
    cursor = None # Initialise cursor

    try:
        # Get data from the request body in JSON format.
        data = request.get_json()

        # Extract values from the request
        threat_name = data.get("threat_name")
        threat_type = data.get("threat_type")
        threat_severity = data.get("threat_severity")
        threat_description = data.get("threat_description")

        # Ensure all required fields are present
        if not threat_name or not threat_type or not threat_severity or not threat_description:
            return jsonify({"error": "Missing required fields"}), 400

        # Establish connection with DB
        connection = get_db_connection()
        cursor = connection.cursor()

        # Check if the threat exists in the DB
        cursor.execute("SELECT * FROM threats WHERE threat_id = %s", (threat_id,))
        existing_threat = cursor.fetchone()

        if not existing_threat:
            return jsonify({"error": "Threat not found"}), 404

        # Update threat logs
        cursor.execute("""
        UPDATE threats
        SET threat_name = %s, threat_type = %s, threat_severity = %s, threat_description = %s
        WHERE threat_id = %s
        """, (threat_name, threat_type, threat_severity, threat_description, threat_id))

        # Commit changes
        connection.commit()

        return jsonify({"message": "Threat updated successfully!"}), 200

    except mysql.connector.Error as err:
        return jsonify({"error": f"MySQL Error: {str(err)}"}), 500 # Handle MySQL connection/query errors.

    except Exception as e:
        return jsonify({"error": f"Error: {str(e)}"}), 500 # Handle any other unexpected errors.

    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None: # To prevent the code from trying to close an object that's not initialised.
            connection.close()


if __name__ == "__main__":
    app.run(debug=True)


