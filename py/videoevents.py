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
import re
import urllib.parse
from datetime import datetime

# Function to convert UTC/EDT time to Eastern Time Zone (EST)
def utc_to_est(time_str):
    # Determine if the time string has the extra `.000Z` format
    if '.000Z' in time_str:
        # Handle ISO format with milliseconds
        time_format = '%Y-%m-%dT%H:%M:%S.%fZ'
        time_zone = 'UTC'
    elif 'Z' in time_str:
        # Handle ISO format without milliseconds
        time_format = '%Y-%m-%dT%H:%M:%SZ'
        time_zone = 'UTC'
    elif 'UTC' in time_str:
        # Handle custom format provided
        time_format = '%m/%d/%y %I:%M:%S %p UTC'
        time_zone = 'UTC'
    elif 'EDT' in time_str:
        # Handle custom format for EDT
        time_format = '%m/%d/%y %I:%M:%S %p EDT'
        time_zone = 'EDT'
    else:
        raise ValueError("Unsupported timezone or format in time string")

    # Parse the time string with the determined format
    time = datetime.strptime(time_str, time_format)

    # Set the timezone
    if time_zone == 'UTC':
        time = time.replace(tzinfo=pytz.utc)
    elif time_zone == 'EDT':
        time = time.replace(tzinfo=pytz.timezone('US/Eastern'))

    # Convert the time to EST
    est_time = time.astimezone(pytz.timezone('US/Eastern'))

    # Format the EST time string
    est_time_str = est_time.strftime('%m/%d/%y %I:%M:%S %p EST')
    return est_time_str

# Function to extract date and time from a string
def extract_datetime(input_str):
    # Regex pattern to match date and time formats
    patterns = [
        r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}Z',  # ISO format with milliseconds
        r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z',          # ISO format without milliseconds
        r'\d{1,2}/\d{1,2}/\d{2} \d{1,2}:\d{2}:\d{2} (AM|PM) UTC'  # Custom format with UTC
    ]
    
    for pattern in patterns:
        match = re.search(pattern, input_str)
        if match:
            return match.group(0)
    
    # If no matching date format found, raise an error
    return input_str



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

# Find all group headers
groups = driver.find_elements(By.TAG_NAME, "h3")

for h3 in groups:
    group_name = h3.text.strip()

    if group_name == "Live TV Channels":
        continue

    # The list is the next <ol> following the h3
    container = h3.find_element(By.XPATH, "following-sibling::div//ol")

    links = container.find_elements(By.TAG_NAME, "a")

    for link in links:
        channel_name = link.text.strip()
        link_url = link.get_attribute("href")

        all_links.append((group_name, channel_name, link_url))

        # print(f"Found link - Group: {group_name}, Name: {channel_name}, URL: {link_url}")


# Print the M3U header
print("#EXTM3U")

# Example usage of extracting and converting time:
for group, name, link in all_links:
    # Navigate to the link URL
    driver.get(link)
    try:
        # Wait for the button to be clickable
        wait = WebDriverWait(driver, 5)
        #try:
            # Try to find loadVideoBtn first
        #    video_button = wait.until(EC.element_to_be_clickable((By.ID, 'loadVideoBtn')))
        #except:
            # If loadVideoBtn is not found, look for loadVideoBtnTwo
        #    video_button = wait.until(EC.element_to_be_clickable((By.ID, 'loadVideoBtn')))
        
        #video_button.click()

        # Wait for a brief period to allow the page to load and network requests to be made
        time.sleep(10)

        # Get all network requests
        network_requests = driver.execute_script("return JSON.stringify(performance.getEntries());")
        
        # Convert the string back to a list of dictionaries in Python
        network_requests = json.loads(network_requests)

        # Filter out only the URLs containing ".m3u8"
        m3u8_urls = [request["name"] for request in network_requests if ".m3u8" in request["name"]]

        cleaned_m3u8_urls = []
        
        for url in m3u8_urls:
            if "ping.gif" in url and "mu=" in url:
                # Extract mu= value
                parsed = urllib.parse.urlparse(url)
                query_params = urllib.parse.parse_qs(parsed.query)
                if "mu" in query_params:
                    # Decode the real .m3u8 URL
                    real_url = urllib.parse.unquote(query_params["mu"][0])
                    cleaned_m3u8_urls.append(real_url)
            else:
                cleaned_m3u8_urls.append(url)

        m3u8_urls = cleaned_m3u8_urls

        # Use the first collected m3u8 URL, or fallback if not found
        if m3u8_urls:
            m3u8_url = m3u8_urls[0]
        else:
            m3u8_url = "https://github.com/mikekaprielian/rtnaodhor93n398/raw/main/en/offline.mp4"

    except Exception as e:
        # If an exception occurs (e.g., button not found), use the default link
        m3u8_url = "https://github.com/mikekaprielian/rtnaodhor93n398/raw/main/en/offline.mp4"

    # Replace invalid characters in the name
    name_fixed = name.replace(',', '')
    name_fixed = name_fixed.replace(': ', ' - ')
    name_parts = name_fixed.split(' - ')
    title = name_parts[0]
    rest_of_title = ' - '.join(name_parts[1:])

    try:
        # Extract the date and time portion from the rest_of_title
        date_time_part = extract_datetime(rest_of_title)

        # Convert to EST
        est_time_str = utc_to_est(date_time_part)
    except ValueError as e:
        # Handle cases where the date extraction fails
        print(f"Error converting time: {e}")
        est_time_str = rest_of_title  # Fall back to displaying the original text

    # Print the channel information in the M3U format
    print(f"#EXTINF:-1 group-title=\"{group}\",{est_time_str} = {title}")
    print(m3u8_url)  # Print only the first m3u8 URL


# Close the WebDriver
driver.quit()


