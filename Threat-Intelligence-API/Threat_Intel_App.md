# Threat Intelligence API🧙🏾
This project is a simple, yet effective Threat Intelligence API designed to track and report various types of 
cybersecurity threats. The API allows users to view known threats, fetch detailed information about specific 
threats, and report new threats. It is backed by a MySQL database and features endpoints to interact with the
data in a meaningful and organised way.

The project demonstrates the application of Flask for building web APIs, SQL for database management, and best
practices in exception handling. The API is designed to be easily extendable and could be further developed to integrate
with threat intelligence platforms or real-time monitoring systems.

## Table of Contents
- [Installation](#installation)
- [Running the Application](#running-the-application)
- [API Endpoints](#api-endpoints)

## Installation
### Access the Repository
The project files are attached to this repository. To run and test the API clone the repository to your local machine:
`git clone <https://github.com/sirenc0de/CFG-Assignments>
cd <CFG-Assignments>`

### Set Up Virtual Environment


### Install Required Dependencies
Install the required Python libraries using pip:
`pip install -r requirements.txt`

### Set Up the Database
- Ensure MySQL is installed and running.
- Use the Threat Intelligence database in MySQL.
- Configure a connection in `config.py`

## Running the Application
- Open file named `db_utils.py` and run to simulate interaction between utility functions and the database, and handle any errors.
- Open file named `app.py` and run to process requests.
- Start the Flask application by running `main.py` file or executing `python main.py` via the terminal to interact with the Threat Intelligence database.
The API will be running on http://127.0.0.1:5000.

## API Endpoints
1. GET /threats: Retrieve a list of known threats.
* URL: http://127.0.0.1:5000/threats

![get_threats_eg.png](images/get_threats_eg.png)

2. GET /threat/<threat_id>: Fetch details of a specific threat.
URL: http://127.0.0.1:5000/threats/<threat_id>
- Replace <threat_id> with the threat's ID (e.g. 7).

![get_threat_by_id_eg.png](images/get_threat_by_id_eg.png)

3. POST /report-threat: Log a new threat to the database.
URL: http://127.0.0.1:5000/report-threat
- Body (JSON): 
`{
"threat_name": "Threat Name",
"threat_type": "Threat Type",
"threat_severity": "Threat severity level",
"threat_description": "Brief description of threat."
}`

![report_threat_eg.png](images/report_threat_eg.png)

4. PUT /update-threat/<threat_id>: Update existing threat record.
URL: http://127.0.0.1:5000/update-threat/<threat_id>

![update_threat_eg.png](images/update_threat_eg.png)

