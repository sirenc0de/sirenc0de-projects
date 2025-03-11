# Import necessary modules from Flask and appropriate utility functions
import mysql.connector
from db_utils import get_db_connection

# Test your connection with MySQL
conn = get_db_connection()
if conn:
    print("Connected to MySQL successfully!")
    conn.close()
else:
    print("Failed to connect to MySQL.")

# Import necessary modules from Flask and appropriate utility functions
from flask import Flask, jsonify, request
from db_utils import get_db_connection

# Initialise the Flask application
app = Flask(__name__)

# API endpoint using a Flask GET route that allows users to retrieve a list of known threats.
@app.route("/threats", methods=["GET"])
def get_threats(): # Get threat intelligence data from the request body and return in JSON format.
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM threats;")
    threats = cursor.fetchall()
    connection.close()
    return jsonify(threats)

# This GET route allows users to fetch the details of a specific threat using threat id.
@app.route("/threat/<int:id>", methods=["GET"])
def get_threat(threat_id): # Get threat intelligence data from the request body filtered using threat id...
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM threats WHERE threat_id = %s;", (threat_id,))
    threat = cursor.fetchone()
    connection.close()
    if threat:
        return jsonify(threat)
    return jsonify({"error": "Threat not found."}), 404

# POST route allows users to report new threats, logging them in the Threat Intelligence DB.
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

# GET route that allows users to filter threats based on their type, severity or simply by name.
@app.route("/threats", methods=["GET"])
def get_threats(): # Get the data from the request body
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

@app.route("/threats/<int:threat_id>", methods=["PUT"])
def update_threat(threat_id):
    connection = None
    cursor = None # to initialise connection and cursor

    try:
        # Get data from the request body
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


