from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium_stealth import stealth
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.os_manager import ChromeType
import random
import time
import json
import pytz
from datetime import datetime

# Function to convert UTC time to Eastern Time Zone (EST)
def utc_to_est(utc_time_str):
    # Extract the time portion from the input string
    time_str = utc_time_str.split(" - ")[-1]
    # Parse the time string as a UTC timezone
    utc_time = datetime.strptime(time_str, "%m/%d/%y %I:%M:%S %p UTC")
    # Convert UTC time to Eastern Time Zone (EST/EDT)
    est_time = utc_time.replace(tzinfo=pytz.utc).astimezone(pytz.timezone('US/Eastern'))
    # Format the EST time string
    est_time_str = est_time.strftime("%m/%d/%y %I:%M:%S %p EST")
    return est_time_str


user_agents = [
    #add your list of user agents here
    'Mozilla/5.0 (Linux; Android 11; Samsung SM-A025G) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19',
    'Mozilla/5.0 (Linux; Android 11; SM-M127N) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/80.0.3987.119 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 11; SM-G998W) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 10; NOH-NX9) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 11; Pixel 5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.111 Mobile Safari/537.36',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) FxiOS/36.0  Mobile/15E148 Safari/605.1.15',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 14_7 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/92.0.4515.90 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 12_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) FxiOS/13.2b11866 Mobile/16A366 Safari/605.1.15',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (iPhone13,3; U; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Mobile/15E148 Safari/602.1 ',
    'Mozilla/5.0 (Linux; Android 11; SM-T227U Build/RP1A.200720.012; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/87.0.4280.141 Safari/537.36',
    'Mozilla/5.0 (Linux; Android 9; KFTRWI) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.88 Safari/537.36',
    'Mozilla/5.0 (Linux; Android 5.0.2; SAMSUNG SM-T550 Build/LRX22G) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/3.3 Chrome/38.0.2125.102 Safari/537.36',
    'Mozilla/5.0 (AppleTV11,1; CPU OS 11.1 like Mac OS X; en-US)',
    'Mozilla/5.0 (Linux; Android 9; AFTSSS Build/PS7228; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/75.0.3770.143 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; U; Android 9.0.0; en-us; TIVO STREAM 4K Build/KOT49H)',
    'Mozilla/5.0 (PlayStation; PlayStation 5/2.26) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; XBOX_ONE_ED) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; Xbox; Xbox One) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2486.0 Safari/537.36 Edge/13.1058',
    'Mozilla/5.0 (Linux; Android 13; SM-G991U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 13; SM-A536U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 13; Pixel 7 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36',

]



chrome_service = Service(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install())


# Set Chrome options
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("start-maximized")
chrome_options.add_argument("disable-infobars")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--crash-dumps-dir=/tmp")

# Randomly select a user agent
user_agent = random.choice(user_agents)
chrome_options.add_argument(f"user-agent={user_agent}")

# Initialize the Chrome WebDriver with the specified options
driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

stealth(
    driver,
    languages=["en-US", "en"],
    vendor="Google Inc.",
    platform="Win32",
    webgl_vendor="Intel Inc.",
    renderer="Intel Iris OpenGL Engine",
    fix_hairline=True,
)

# Open the webpage
url = "https://thetvapp.to/"
driver.get(url)

# Wait for the page to load
wait = WebDriverWait(driver, 10)
wait.until(EC.presence_of_element_located((By.CLASS_NAME, "row")))

# Find all the rows containing the desired links
rows = driver.find_elements(By.CLASS_NAME, "row")

# Initialize a list to store the links
all_links = []

# Iterate over each row
for row in rows:
    # Find the group name (e.g., MLB)
    group_name = row.find_element(By.TAG_NAME, "h3").text
    
    # Check if it's not Live TV Channels
    if group_name != "Live TV Channels":
        # Find all links in the row
        links = row.find_elements(By.TAG_NAME, "a")
        
        # Iterate over each link
        for link in links:
            # Get the channel name
            channel_name = link.text.strip()
            
            # Get the link URL and add it to the list
            link_url = link.get_attribute("href")
            all_links.append((group_name, channel_name, link_url))

# Print the M3U header
print("#EXTM3U")

# Iterate over each link
for group, name, link in all_links:
    # Navigate to the link URL
    driver.get(link)

    # Wait for a brief period to allow the page to load and network requests to be made
    time.sleep(1)

    # Get all network requests
    network_requests = driver.execute_script("return JSON.stringify(performance.getEntries());")

    # Convert the string back to a list of dictionaries in Python
    network_requests = json.loads(network_requests)

    # Get all network requests
    #network_requests = driver.execute_script("return performance.getEntries();")

    # Filter out only the URLs containing ".m3u8"
    m3u8_urls = [request["name"] for request in network_requests if ".m3u8" in request["name"]]

    # Print the collected m3u8 URLs
    if m3u8_urls:
     name_fixed = name.replace(',', '')
     name_fixed = name_fixed.replace(': ', ' - ')
     name_parts = name_fixed.split(' - ')
     title = name_parts[0]
     rest_of_title = ' - '.join(name_parts[1:])
     est_time_str = utc_to_est(rest_of_title)
     print(f"#EXTINF:-1 group-title=\"{group}\", {title} = {est_time_str}")
     print(m3u8_urls[0])  # Print only the first m3u8 URL


# Close the WebDriver
driver.quit()

