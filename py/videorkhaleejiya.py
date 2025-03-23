import subprocess
import json

def get_channel_token(kwik_key, media_url):
    # Construct the cURL command
    curl_command = [
        "curl",
        "-X", "POST",
        "https://rotana.net/channels/generateAclToken",
        "-H", "Referer: https://rotana.net/",
        "-H", "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
        "-H", "Content-Type: application/x-www-form-urlencoded; charset=UTF-8",
        "-H", "X-Forwarded-For: 216.239.80.141",
        "--data-urlencode", f"kwik_key={kwik_key}",
        "--data-urlencode", f"mediaUrl={media_url}"
    ]

    # Execute the cURL command
    try:
        result = subprocess.run(curl_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        result.check_returncode()  # Raises an error if curl fails
        response_json = json.loads(result.stdout)  # Parse JSON response
        return response_json.get('data')  # Extract token
    except subprocess.CalledProcessError as e:
        print(f"cURL command failed with error:\n{e.stderr}")
        return None
    except json.JSONDecodeError:
        print("Failed to parse JSON response")
        return None

def construct_m3u8_link(media_url, acl_token):
    return f"https://live.kwikmotion.com/{media_url}live/{media_url}.smil/playlist.m3u8?hdnts={acl_token}"

# Fetch the kwik_key and media_url
kwik_key = "5c6f48285bb30cc477408af69876cd6b"
media_url = "rkhalijeah"

if kwik_key:
    acl_token = get_channel_token(kwik_key, media_url)
    if acl_token:
        m3u8_link = construct_m3u8_link(media_url, acl_token)
        print("M3U8 Link:", m3u8_link)
    else:
        print("Failed to retrieve ACL token")
else:
    print("Failed to retrieve kwik_key from the page")
