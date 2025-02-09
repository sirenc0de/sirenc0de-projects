from fileinput import filename

import requests
import json

print("\nWelcome to the Criminal Threat Checker (CTC).\nThis console application is designed to interact with the UK Police API to retrieve crime trends in major cities.")

# Step 1: fetch all available UK police forces
def get_police_forces():
    """Fetches and prints all available UK Police Forces."""
    url = "https://data.police.uk/api/forces" # API endpoint for fetching crime categories
    response = requests.get(url)

    if response.status_code == 200:
        forces = response.json()
        print("\nAvailable Police Forces: ")
        for force in forces:
            print(f"{force['id']}: {force['name']}")
        return {force['id']: force['name'] for force in forces} # to list all UK police forces
    else:
        print("Error: " .format(response.status_code, response.text))
        return {}

# Step 2: Fetch crimes for a chosen police force by city
def fetch_crimes_by_force(force_id):
    """Fetches crimes for specific UK police force."""
    force_id_slice = force_id[:5] # to slice the first 5 characters of the force ID
    url = f"https://data.police.uk/api/crimes-no-location?category=all-crime&force={force_id}"
    response = requests.get(url)

    if response.status_code == 200:
        crimes = response.json()
        return crimes[:5] # to return first 5 crimes
    else:
        print(f"Error: " .format(response.status_code, response.text))
        return [] # to return empty list if an error occurs

# Step 3: Save crime data to a JSON file
def save_to_json(crimes, force_id):
    """Saves data to a JSON file in readable format."""
    sort_choice = input("\nAdd the option to sort the crimes by category? (Yes/No)? ").strip().lower()
    if sort_choice == 'Yes':
        sorted_crimes = sorted(crimes, key=lambda x: x["category"]) # to sort crimes by category facilitated by python's inbuilt function, sorted()
    else:
        sorted_crimes = sorted(crimes, key=lambda x: x["date"]) # sort crimes by date of offence, if available

    with open(f"crimes_{force_id}.json", "w") as file:
        json.dump(sorted_crimes, file, indent=4)
        print(f"\n✅Great! Your crime data successfully saved to {force_id}_crimes.json")

# Step 4: Main program
def main():
    forces = get_police_forces()
    if not forces:
        print("❌No police forces found. Exiting program.")
        return

    user_choice = input("\nEnter the police force ID you want to investigate, from the list above: ").strip().lower() # in-built functions
    if user_choice in forces:
        crimes = fetch_crimes_by_force(user_choice)
        if crimes:
            print(f"\n🔎 First 5 crimes reported in {forces[user_choice]} (ID Slice: {user_choice[:5]}):\n")
            for crime in crimes:
                crime_id = crime.get('persistent_id', 'N/A') # .get() used to retrieve 'persistent id'
                crime_id = crime_id[:8] if crime_id != 'N/A' else crime_id # slice to 8 characters where applicable
                print(f"- {crime['category'].title()} (Crime ID: {crime_id}")
            save_to_json(crimes, f"{user_choice}_crimes.json")
        else:
            print("Whoops! No crimes found for this police force. Don't fret, that's a good thing!")
    else:
        print("Uh-Oh! Invalid police force ID. Please restart and again.")

# Run the program!
if __name__ == "__main__":
    main()






