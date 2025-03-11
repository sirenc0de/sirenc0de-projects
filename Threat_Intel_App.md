# Threat Intelligence API🧙🏾
This project is a simple, yet powerful Threat Intelligence API designed to track and report various types of 
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
- [Testing the API](#testing-the-api)

## Access the Repository
The project files are attached to this repository. To run and test the API clone the repository to your local machine:
`git clone <https://github.com/sirenc0de/CFG-Assignments>
cd <CFG-Assignments>`

### Install Required Dependencies
Install the required Python libraries using pip:
`pip install -r requirements.txt`

### Running the Application
Start the Flask application by running main.py file or executing `python main.py` via the terminal.
The API will be running on http://127.0.0.1:5000.

## API Endpoints
* GET /threats: Retrieve a list of known threats.

* GET /threat/<threat_id>: Fetch details of a specific threat.
* POST /report-threat: Log a new threat to the database.
* PUT /update-threat/<threat_id>: Update existing threat record.

## Testing the API
