import re
import requests

def extract_m3u8_link(url):
    headers = {
        'Referer': 'https://www.chch.com'
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()

    # Extract the JavaScript code containing the m3u8 link
    javascript_code = response.text

    # Use regular expressions to find the m3u8 link
    match = re.search(r"src: '([^']+)'", javascript_code)
    if match:
        m3u8_link = match.group(1)
        return m3u8_link
    else:
        raise ValueError("m3u8 link not found")

# Example usage
url = 'https://chch.cdn.clearcable.net/'
m3u8_link = extract_m3u8_link(url)
print(m3u8_link)
