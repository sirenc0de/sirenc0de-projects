# Import necessary modules and MySQL connector
from dbm import error

import mysql.connector
from flask import jsonify, request
from config import DB_CONFIG

# Connect to the database
def get_db_connection():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except mysql.connector.Error as err:
        return None, f"Database connection failed: {err}"

# 1. Retrieve all threat records
def get_threats():
    conn, error = get_db_connection()
    if error:
        return jsonify({"error": error}), 500

    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM threats")
        threats = cursor.fetchall()
        conn.close()
        return jsonify(threats), 200
    except mysql.connector.Error as err:
        conn.close()
        return jsonify({"error": f"Error fetching threats: {err}"}), 500

# 2. Fetch a specific threat by ID
def get_threat_by_id(threat_id):
    conn, error = get_db_connection()
    if error:
        return jsonify({"error": error}), 500

    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM threats WHERE threat_id = %s", threat_id,)
        threat = cursor.fetchone()
        conn.close()

        if threat:
            return jsonify(threat), 200
        return jsonify({"error": "Threat not found!"}), 404
    except mysql.connector.Error as err:
        conn.close()
        return jsonify({"error": f"Error fetching threat: {err}"}), 500

# 3. Log a new threat
def report_threat():
    data = request.get_json()
    conn, error = get_db_connection()
    if error:
        return jsonify({"error": error}), 500

    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO threats (threat_name, threat_type, threat_severity, threat_description, reported_date) VALUES (%s, %s, %s, %s, NOW())",
            (data["threat_name"], data["threat_type"], data["threat_severity"], data["threat_description"]),
        )
        conn.commit()
        conn.close()
        return jsonify({"message": "Threat reported successfully!"}), 200
    except mysql.connector.Error as err:
        return jsonify({"error": f"Error reporting threat: {err}"}), 500

# 4. Update an existing threat log
def update_threat(threat_id):
    data = request.get_json()
    conn, error = get_db_connection()
    if error:
        return jsonify({"error": error}), 500

    try:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE threats SET threat_name= %s, threat_type= %s, threat_severity= %s, threat_description= %s WHERE threat_id= %s",
            (data["threat_name"], data["threat_type"], data["threat_severity"], data["threat_description"], threat_id),
        )

        conn.commit()
        conn.close()
        return jsonify({"message": "Threat updated successfully!"}), 200
    except mysql.connector.Error as err:
        conn.close()
        return jsonify({"error": f"Error updating threat: {err}"}), 500

