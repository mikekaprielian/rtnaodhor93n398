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
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 17_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/126.0.6478.35 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.6422.165 Mobile Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:127.0) Gecko/20100101 Firefox/127.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 14.5; rv:127.0) Gecko/20100101 Firefox/127.0',
    'Mozilla/5.0 (X11; Linux i686; rv:127.0) Gecko/20100101 Firefox/127.0',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 14_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) FxiOS/127.0 Mobile/15E148 Safari/605.1.15',
    'Mozilla/5.0 (Android 14; Mobile; rv:127.0) Gecko/126.0 Firefox/126.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:115.0) Gecko/20100101 Firefox/115.0',


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

