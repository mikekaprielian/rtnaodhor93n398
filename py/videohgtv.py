from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

url = "https://thetvapp.to/tv/mtv-live-stream/"


def extract_desired_url(requests):
    # Search for the desired URL in the requests
    for request in requests:
        if "MTVEast.m3u8?token=" in request:
            return request
    return None


def get_get_requests():
    try:
        # Execute JavaScript to capture network requests
        requests = driver.execute_script("""
            var performance = window.performance || window.webkitPerformance || window.msPerformance || window.mozPerformance;
            if (!performance) {
                return [];
            }
            var entries = performance.getEntriesByType("resource");
            var urls = [];
            for (var i = 0; i < entries.length; i++) {
                urls.push(entries[i].name);
            }
            return urls;
        """)
        return requests
    except Exception as e:
        print("An error occurred:", e)
        return None
    finally:
        driver.quit()


# Set Chrome options
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # To run Chrome in headless mode

# Initialize Selenium WebDriver with the service and Chrome options
driver = webdriver.Chrome(options=options)

# Navigate to the URL
driver.get(url)

# Wait for the video player element to be present
try:
    video_player = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "video-player")))
    print("Video player loaded successfully.")
except:
    pass  # Do nothing if the video player is not found, the message will not be printed


# Call the function to get GET requests
get_requests = get_get_requests()

# Extract the desired URL
if get_requests:
    desired_url = extract_desired_url(get_requests)
    if desired_url:
        print("Desired URL found:", desired_url)
        # Write the desired URL to the file
        with open("mtvurl.txt", "w") as file:
            file.write(desired_url)
            print("Desired URL written to mtvurl.txt")
    else:
        print("No desired URL found in the requests.")
else:
    print("No GET requests found.")
