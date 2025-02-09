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

def fetch_cyber_crime(lat, lng, date="2024-01"):
    url = "https://data.police.uk/api/crimes-street/all-crime"
    params = {
        "lat": lat, # Latitude
        "lng": lng, # Longitude
        "date": date, # Format: YYYY-MM
    }

    print("Requesting data from:" .format(url))
    print("Params: " .format(params))

    response = requests.get(url, params=params)
    print("Response Status Code: " .format(response.status_code))

    if response.status_code == 200:
        try:
            crimes = response.json()
            print("Raw API Response: " .format(crimes))

            if not crimes:
                print("No crimes found for this location and date.")
                return []
            # Extract and print all unique crime categories
            categories = set(crime['category']for crime in crimes)
            print("Crime categories found: " .format(categories))

            cyber_crimes = [crime for crime in crimes if "cyber" in crime['category'] .lower()]
            print("Filtered Cyber Crimes: " .format(cyber_crimes))

            return cyber_crimes
        except json.JSONDecodeError:
            print("Error: Could not decode JSON response.")
            print(response.text) # print raw response if JSON fails
            return []

# Call function
lat1, lng2 = "51.5074", "-0.1278" # London coordinates
date_of_cr = "2023-12"
cyber_crimes_detected = fetch_cyber_crime(lat1, lng2, date_of_cr)
print("Threat Scanner Results: ", cyber_crimes_detected)



