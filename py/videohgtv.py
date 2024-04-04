from selenium import webdriver
from selenium_stealth import stealth
from selenium.webdriver.common.by import By
import time
import random


user_agents = [
    #add your list of user agents here
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
]




# Path to the ChromeDriver executable
chromedriver_path = '/usr/local/bin/chromedriver'

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





user_agent = random.choice(user_agents)
chrome_options.add_argument(f"user-agent={user_agent}")


# Initialize the Chrome WebDriver with the specified options
driver = webdriver.Chrome(executable_path=chromedriver_path, options=chrome_options)


stealth(
    driver,
    languages=["en-US", "en"],
    vendor="Google Inc.",
    platform="Win32",
    webgl_vendor="Intel Inc.",
    renderer="Intel Iris OpenGL Engine",
    fix_hairline=True,
)

# Navigate to the webpage
url = "https://thetvapp.to/tv/hgtv-live-stream/"  # Corrected URL
driver.get(url)

# Wait for a brief period to allow the page to load and network requests to be made
time.sleep(1)

# Get all network requests
network_requests = driver.execute_script("return performance.getEntries();")

# Filter out only the URLs containing ".m3u8"
m3u8_urls = [request["name"] for request in network_requests if ".m3u8" in request["name"]]

# Write URLs to a text file
#with open("network_responses.txt", "w") as file:
#   for url in m3u8_urls:
#        file.write(url + "\n")

# Print the first URL if there is at least one
if m3u8_urls:
    print(m3u8_urls[0])

# Quit the WebDriver
driver.quit()
