# This console application is designed to interact with the UK Police API to retrieve cyber-related crime trends in major cities.

import requests
# API endpoint for fetching crime categories
URL = "https://data.police.uk/docs/"
# testing api
response = requests.get("https://data.police.uk/docs/")

if response.status_code == 200:
    print("API is working")
else:
    print(f"Error: {response.status_code}")

# Fetch crime data


