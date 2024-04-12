from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium_stealth import stealth
import random
import os
import time

# Set Firefox options
firefox_options = webdriver.FirefoxOptions()
firefox_options.add_argument("--headless")
firefox_options.add_argument("--disable-gpu")
firefox_options.add_argument("--no-sandbox")
firefox_options.add_argument("--disable-dev-shm-usage")

# Randomly select a user agent
user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/97.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0',
    # Add more user agents as needed
]
user_agent = random.choice(user_agents)
firefox_options.add_argument(f"user-agent={user_agent}")

# Create the Firefox WebDriver instance
driver = webdriver.Firefox(options=firefox_options)

# Apply stealth features
stealth(driver,
    languages=["en-US", "en"],
    vendor="Google Inc.",
    platform="Win32",
    webgl_vendor="Intel Inc.",
    renderer="Intel Iris OpenGL Engine",
    fix_hairline=True
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
    time.sleep(10)

    # Get all network requests
    network_requests = driver.execute_script("return performance.getEntries();")

    # Filter out only the URLs containing ".m3u8"
    m3u8_urls = [request["name"] for request in network_requests if ".m3u8" in request["name"]]

    # Print the collected m3u8 URLs
    if m3u8_urls:
        print(f"#EXTINF:-1 group-title=\"{group}\", {name}")
        print(m3u8_urls[0])  # Print only the first m3u8 URL

# Close the WebDriver
driver.quit()
