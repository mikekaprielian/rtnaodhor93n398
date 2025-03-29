import subprocess
import re
import base64
import json

def get_page_content(target_url):
    """Function to fetch the page content using cURL."""
    curl_command = [
        "/snap/bin/curl",  # Full path to curl
        "-s",  # Silent mode (no progress bar)
        "-X", "GET",  # GET method
        target_url,  # URL passed to the function
        "-H", "Referer: https://rotana.net/",
        "-H", "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
        "-H", "Content-Type: application/x-www-form-urlencoded; charset=UTF-8",
        "-H", "X-Forwarded-For: 216.239.80.141"
    ]
    
    try:
        # Execute cURL command
        result = subprocess.run(curl_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, encoding='utf-8')
        result.check_returncode()  # Ensure cURL ran successfully
        return result.stdout  # Return the page content
    except subprocess.CalledProcessError as e:
        print(f"cURL command failed with error:\n{e.stderr}")
        return None  # Return None if an error occurs

# Target webpage URL
target_url = "https://rotana.net/live/cinema"

# Fetch the page content using the function
page_content = get_page_content(target_url)

if not page_content:
    print("Failed to retrieve page content.")
    exit()

# Extract the Base64 config string from JavaScript
match = re.search(r"var config = '([^']+)'", page_content)
if not match:
    print("Failed to extract Base64 config string.")
    exit()

# Decode Base64 string
config_json = base64.b64decode(match.group(1)).decode("utf-8")
config_data = json.loads(config_json)

# Extract M3U8 URL
m3u8_url = config_data.get("stream", {}).get("url")
if m3u8_url:
    print(m3u8_url)
else:
    print("Failed to extract M3U8 URL.")
