from flask import Flask
from db_utils import get_threats, get_threat_by_id, report_threat, update_threat

# Initialise the Flask application
app = Flask(__name__)

# API Endpoint 1: Retrieve a list of all known threats (with optional filters).
@app.route("/threats", methods=["GET"])
def retrieve_threats():
    return get_threats()

# API Endpoint 2: Fetch the details of a specific threat.
@app.route("/threat/<int:threat_id>", methods=["GET"])
def retrieve_threat(threat_id):
    return get_threat_by_id(threat_id)

# API Endpoint 3: Report a new threat.
@app.route("/report-threat", methods=["POST"])
def log_threat():
    return report_threat()

# API Endpoint 4: Update an existing threat.
@app.route("/threats/<int:threat_id>", methods=["PUT"])
def update_existing_threat(threat_id):
    return update_threat(threat_id)

if __name__ == "__main__":
    app.run(debug=True)


