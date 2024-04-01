import requests
import re

url = "https://www.qub.ca/tvaplus/tva/en-direct?silent_auth=true"

try:
    # Send GET request
    response = requests.get(url)
    # Check if request was successful
    response.raise_for_status()
    # Extract videoSourceUrl using regular expressions
    match = re.search(r'"videoSourceUrl":"([^"]+)"', response.text)
    
    # Output the videoSourceUrl if found
    if match:
        video_source_url = match.group(1)
        print(video_source_url)
    else:
        print("No videoSourceUrl found")
except requests.exceptions.RequestException as e:
    # Handle any errors that occurred during the request
    print("Request failed:", e)
