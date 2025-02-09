# from http.client import responses
# from pydoc import resolve

import requests

# app = Cyber Threat Scanner
# This console application is designed to interact with the UK Police API to retrieve cyber-related crime trends in major cities.

# API endpoint for fetching crime categories
URL = "https://data.police.uk/docs/"
# # testing api
# response = requests.get("https://data.police.uk/docs/")
#
# if response.status_code == 200:
#     print("API is working")
# else:
#     print(f"Error: {response.status_code}")

import json

# def fetch_cyber_crime(lat, lng, date="2024-12"):
#     url = "https://data.police.uk/api/crimes-street/all-crime"
#     params = {
#         "lat": lat, # Latitude
#         "lng": lng, # Longitude
#         "date": date, # Format: YYYY-MM
#     }
#     response = requests.get(url, params=params)

#     if response.status_code == 200: # HTTP status code successful
#         crimes = response.json()
#         cyber_crimes = [crime for crime in crimes if "cyber" in crime['category'].lower()]
#         return cyber_crimes
#     else:
#         return f"Error: {response.status_code}, {response.text}"
#
# # call function to test it
# lat, lng = "51.5074", "-0.1278" # Coordinates for the City of London
# cyber_crimes = fetch_cyber_crime(lat, lng)
#
# print(cyber_crimes)

# Return empty list [] meaning there were no 'cyber' crimes in London during 2024-12, review all crime categories

# def fetch_crime_cats(lat, lng):
#     url = "https://data.police.uk/api/crimes-street/all-crime"
#     params = {"lat": lat,"lng": lng} # lat for Latitude and lng for Longitude
#
#     response = requests.get(url, params=params)
#
#     if response.status_code == 200:
#         crimes = response.json()
#         categories = set(crime['category'] for crime in crimes)
#         print("Available crime categories: " .format(categories)) # print all categories
#
#     else:
#         print("Error: " .format(response.status_code, response.text))

# Test function
# lat1, lng2 = ("52.4862", "-1.8904")
# fetch_crime_cats(lat1, lng2)

# function operational but still not returning crime data in given locations, test to see if this is related to a security issue and that the API data does not require a "Police Force ID"

def get_police_forces():
    """Fetches and prints all available UK Police Forces."""
    url = "https://data.police.uk/api/forces"
    response = requests.get(url)

    if response.status_code == 200:
        forces = response.json()
        print("\nAvailable Police Forces")
        for force in forces:
            print(f"{force['id']}: {force['name']}") # to list all UK police forces, as a dictionary
    else:
        print("Error: " .format(response.status_code, response.text))
        return {}

def fetch_crimes_with_force(force_id):
    """Fetches and prints crimes for the chosen UK Police Force."""
    url = f"https://data.police.uk/api/crimes-no-location?category=all-crimes&force={force_id}"
    response = requests.get(url)

    if response.status_code == 200:
        crimes = response.json()
        print(f"\nCrimes for {force_id} ({force_dict[force_id]}): ")
        print(crimes[:5]) # to print the first 5 crimes
    else:
        print(f"Error: " .format(response.status_code, response.text))

# Step 1: Get police forces
force_dict = get_police_forces()

# Debugging - check input is captured
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










