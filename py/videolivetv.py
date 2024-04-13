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


user_agents = [
    #add your list of user agents here
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
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

# Find the Live TV Channels row
live_tv_row = driver.find_element(By.XPATH, "//h3[contains(text(), 'Live TV Channels')]/..")

# Find all links in the Live TV Channels row
links = live_tv_row.find_elements(By.TAG_NAME, "a")

# Initialize a list to store the links
live_tv_links = []

# Iterate over each link
for link in links:
    # Get the channel name
    channel_name = link.text.strip()
    
    # Get the link URL and add it to the list
    link_url = link.get_attribute("href")
    live_tv_links.append((channel_name, link_url))

# Print the M3U header
print("#EXTM3U")

# Iterate over each live TV channel link
for name, link in live_tv_links:
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

    # Print the collected m3u8 URL
    if m3u8_urls:
        print(f"#EXTINF:-1 group-title="USA TV" tvg-name=\"{name}\", {name}")
        print(m3u8_urls[0])  # Print only the first m3u8 URL

# Close the WebDriver
driver.quit() 

