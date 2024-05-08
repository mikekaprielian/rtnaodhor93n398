import requests
import re

url = "https://www.qub.ca/tvaplus/tva/en-direct?silent_auth=true"

try:
    # Send GET request to get the page content
    response = requests.get(url)
    response.raise_for_status()
    
    # Extract videoSourceUrl using regular expressions
    match = re.search(r'"videoSourceUrl":"([^"]+)"', response.text)
    
    if match:
        video_source_url = match.group(1).replace('\\u0026', '&')  # Clean the URL if necessary
        #print("Video source URL found:", video_source_url)
        
        # Fetch the M3U8 file content
        m3u8_response = requests.get(video_source_url)
        m3u8_response.raise_for_status()
        
        # Print the content of the M3U8 file
        print("Content of M3U8 file:")
        print(m3u8_response.text)
    else:
        print("No videoSourceUrl found")
except requests.exceptions.RequestException as e:
    print("Request failed:", e)
