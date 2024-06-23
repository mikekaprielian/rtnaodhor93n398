import requests
import json

def get_m3u8_link(api_url, x_forwarded_for):
    headers = {
        'X-Forwarded-For': x_forwarded_for
    }

    # Fetch the JSON response from the API with the X-Forwarded-For header
    response = requests.get(api_url, headers=headers)
    response.raise_for_status()
    data = response.json()

    # Extract the necessary parts from the JSON
    service_url = data["Media"]["Link"]["ServiceUrl"]
    secure_path = data["Media"]["Link"]["SecurePath"]

    # Fix the secure path to decode unicode escape sequences
    secure_path = secure_path.encode('utf-8').decode('unicode_escape')

    # Construct the final M3U8 link
    final_m3u8_link = f"{service_url}{secure_path}"

    #final_m3u8_link = final_m3u8_link.replace("/cnnturknp/playlist.m3u8?", "/cnnturknp/track_4_1000/playlist.m3u8?")

    return final_m3u8_link


    


# URL provided in the request
api_url = "https://www.cnnturk.com/api/cnnvideo/media?id=62d6814670380e2cdc7c124c&isMobile=true"
# Example IP address to use in the X-Forwarded-For header
x_forwarded_for = "216.239.80.141"

# Get the final M3U8 link
try:
    m3u8_link = get_m3u8_link(api_url, x_forwarded_for)
    print(m3u8_link)
except KeyError as e:
    print(f"Error: {e}")
