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

def fetch_cyber_crime(lat, lng, date="2023-02"):
    url = "https://data.police.uk/api/crimes-street/all-crime"
    params = {
        "lat": lat, # Latitude
        "lng": lng, # Longitude
        "date": date, # Format: YYYY-MM
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        crimes = response.json()

        # Debugging: print the raw api response
        print("Raw API Response: ", crimes)

        cyber_crimes = [crime for crime in crimes if "cyber" in crime['category'].lower()]
        return cyber_crimes
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return []










