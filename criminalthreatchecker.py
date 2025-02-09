# from http.client import responses
# from pydoc import resolve

import requests
import json

# app = Criminal Threat Checker (CTC)
# This console application is designed to interact with the UK Police API to retrieve different crime trends in major cities.

def get_police_forces():
    """Fetches and prints all available UK Police Forces."""
    url = "https://data.police.uk/api/forces" # API endpoint for fetching crime categories
    response = requests.get(url)

    if response.status_code == 200:
        forces = response.json()
        print("\nAvailable Police Forces")
        for force in forces:
            print(f"{force['id']}: {force['name']}")
        return {force['id']: force['name'] for force in forces} # to list all UK police forces, as a dictionary
    else:
        print("Error: " .format(response.status_code, response.text))
        return {}

def fetch_crimes_with_force(force_id: str):
    """Fetches crimes for specific UK police force."""
    force_id_slice = force_id[:5] # to slice the first 5 characters of the force ID
    """Fetches and prints crimes for the chosen UK Police Force."""
    url = f"https://data.police.uk/api/crimes-no-location?category=all-crimes&force={force_id}"
    response = requests.get(url)

    if response.status_code == 200:
        crimes = response.json()
        print(f"\nCrimes for {force_id_slice} ({force_dict[force_id]}): ") # use slice ID
        print(crimes[:5]) # to print the first 5 crimes
        return crimes # to return the list of crimes
    else:
        print(f"Error: " .format(response.status_code, response.text))
        return [] # to return empty list if an error occurs

def save_crimes_to_json(crimes, force_id):
    try:
        with open(f"crimes_{force_id}.json", "w", encoding="utf-8") as file:
            json.dump(crimes, file, indent=4)
            print(f"Crime data saved to crimes_{force_id}.json")
    except Exception as e:
        print(f"Error saving file: {e}")

# main program flow
force_dict = get_police_forces()

if not force_dict:
    print("No police forces found. Exiting program.")
    exit()

user_choice = input("\nEnter the required Police Force ID from the list above: ").strip().lower()
print("User entered: " .format(user_choice)) # debugging step

# Step 2: Fetch and display crime data for the chosen force
if user_choice in force_dict:
     fetch_crimes_with_force(user_choice)
else:
     print("Police Force ID invalid. Please try again.")








