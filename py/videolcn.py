import re
import requests

def extract_policy_key(video_url):
    # Extract player ID, account ID, and video ID from the video URL
    match = re.search(r'players\.brightcove\.net/(\d+)/([^/]+)_([^/]+)/index.html\?videoId=(\d+)', video_url)
    if not match:
        raise ValueError("Invalid Brightcove video URL")

    account_id, player_id, embed, video_id = match.groups()

    # Construct the base URL
    base_url = 'http://players.brightcove.net/%s/%s_%s/' % (account_id, player_id, embed)

    # Download the webpage to extract the policy key
    webpage_url = base_url + 'index.min.js'
    webpage_content = requests.get(webpage_url).text

    # Try to extract the policy key from the webpage
    policy_key_match = re.search(r'policyKey\s*:\s*(["\'])(.+?)\1', webpage_content)
    if policy_key_match:
        policy_key = policy_key_match.group(2)
        return policy_key
    else:
        raise ValueError("Policy key not found")

def fetch_m3u8_url(video_id, policy_key):
    api_url = f"https://edge.api.brightcove.com/playback/v1/accounts/1116875978001/videos/{video_id}"
    headers = {'Accept': f'application/json;pk={policy_key}'}
    response = requests.get(api_url, headers=headers)
    response_data = response.json()
    m3u8_url = None
    for source in response_data.get('sources', []):
        if source.get('src'):
            m3u8_url = source['src']
            break
    return m3u8_url

# Example usage
video_url = 'https://players.brightcove.net/1116875978001/rkQ1RPRsf_default/index.html?videoId=6341614265112'
policy_key = extract_policy_key(video_url)
#print("Policy key:", policy_key)

video_id = re.search(r'videoId=(\d+)', video_url).group(1)
m3u8_url = fetch_m3u8_url(video_id, policy_key)
print(m3u8_url)
