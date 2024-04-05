import requests
import base64

url = "https://www.elahmad.com/tv/result/embed_result_76.php"
referer = "http://www.elahmad.com/tv/radiant.php?id=lbc_1"
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.5304.87 Safari/537.36"
data = {"id": "lbc_1"}

headers = {
    "Referer": referer,
    "User-Agent": user_agent
}

response = requests.post(url, headers=headers, data=data)

if response.status_code == 200:
    try:
        result_json = response.json()
        link = result_json.get('link')
        if link:
            decoded_result = base64.b64decode(link).decode('utf-8')
            print(decoded_result)
        else:
            print("Error: 'link' field not found in the response")
    except Exception as e:
        print("Error:", e)
else:
    print("Error:", response.status_code)
