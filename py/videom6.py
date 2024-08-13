import requests
import re

url = "https://www.livehdtv.com/token.php?stream=m6"
headers = {
    "Referer": "https://www.livehdtv.com",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
}

try:
    # Send GET request with headers
    response = requests.get(url, headers=headers)
    # Check if the request was successful
    response.raise_for_status()
    # Extract the m3u8 link from the script within the HTML response
    m3u8_links = re.findall(r'file:\s*"([^"]+\.m3u8[^"]*)"', response.text) 

    # Output the first m3u8 link found
    if m3u8_links:
        print(m3u8_links[0])
    else:
        print("No M3U8 link found")
except requests.exceptions.RequestException as e:
    # Handle any errors that occurred during the request
    print("Request failed:", e)
