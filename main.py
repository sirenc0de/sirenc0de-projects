# Import necessary modules
from random import choice
import requests

BASE_URL = "http://127.0.0.1:5000" # Ensure this matches your Flask API URL

def welcome():
    print("\n🔹 Welcome to the Threat Intelligence API 🔹\n")
    print("Options:")
    print("1. View all threats")
    print("2. View a specific threat")
    print("3. Report a new threat")
    print("4. Update an existing threat")
    print("5. Exit!")

# 1. Retrieve all threats
def get_all_threats():
    response = requests.get(f"{BASE_URL}/threats")
    print("🔹 All Threats:", response.json())

# 2. Fetch details of a specific threat
def get_threat_by_id():
    threat_id = input("Enter the Threat ID: ")
    response = requests.get(f"{BASE_URL}/threat/{threat_id}")
    print(f"🔹 Threat {threat_id} Details:", response.json())

# 3. Report a new threat
def report_threat():
    threat_name = input("Enter threat name: ")
    threat_type = input("Enter threat type: ")
    threat_severity = input("Enter severity (Low/Medium/High/Critical): ")
    threat_description = input("Enter a brief description of the threat: ")

    new_threat = {
        "threat_name": threat_name,
        "threat_type": threat_type,
        "threat_severity": threat_severity,
        "threat_description": threat_description,
    }

    response = requests.post(f"{BASE_URL}/report-threat", json=new_threat)
    print("🔹 Threat Report Response:", response.json())

# 4. Update a threat log
def update_threat():
    threat_id = input("Enter the Threat ID to update record: ")
    threat_name = input("Updated threat name: ")
    threat_type = input ("Updated threat type: ")
    threat_severity = input("Updated severity (Low/Medium/High/Critical): ")
    threat_description = input("Updated description: ")

    update_data = {
        "threat_name": threat_name,
        "threat_type": threat_type,
        "threat_severity": threat_severity,
        "threat_description": threat_description,
    }

    response = requests.put(f"{BASE_URL}/update-threat/{threat_id}", json=update_data)
    print(f"🔹 Update Threat {threat_id} Response:", response.json())

# Run Flask application
if __name__ == "__main__":
    while True:
        welcome()
        choice = input("Select an option (1-5): ")

        if choice == "1":
            get_all_threats()
        elif choice == "2":
            get_threat_by_id()
        elif choice == "3":
            report_threat()
        elif choice == "4":
            update_threat()
        elif choice == "5":
            print("\nExiting... Goodbye!👋")
            break
        else:
            print("\n⚠️ Invalid choice, please try again!\n")



