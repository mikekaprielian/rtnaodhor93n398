import requests
import re
import json

url = "https://mediainfo.tf1.fr/mediainfocombo/L_LCI?format=hls"

try:
    # Send GET request
    response = requests.get(url)
    # Check if request was successful
    response.raise_for_status()
    # Parse JSON response
    data = json.loads(response.text)

    # Extract M3U8 URL from JSON
    m3u8_url = data.get("delivery", {}).get("url")
    
    if m3u8_url:
        print(m3u8_url)
    else:
        print("No M3U8 URL found in the JSON response.")
        
except requests.exceptions.RequestException as e:
    # Handle any errors that occurred during the request
    print("Request failed:", e)
