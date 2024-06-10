import time
from DrissionPage import ChromiumPage, ChromiumOptions

def pass_cycle(_driver: ChromiumPage):
    """Function to pass the Cloudflare challenge."""
    try:
        iframe = _driver('xpath://div/iframe')
        checkbox = iframe.s_ele("xpath://input[@type='checkbox']")
        if checkbox is not None:
            checkbox.click()
    except Exception as e:
        print(f"Exception in pass_cycle: {e}")
        pass

if __name__ == '__main__':
    # Chromium Browser Path
    browser_path = r"/usr/bin/google-chrome"

    options = ChromiumOptions()
    #options.set_paths(browser_path=browser_path)

    arguments = [
        "--no-first-run",
        "--force-color-profile=srgb",
        "--metrics-recording-only",
        "--password-store=basic",
        "--use-mock-keychain",
        "--export-tagged-pdf",
        "--no-default-browser-check",
        "--disable-background-mode",
        "--enable-features=NetworkService,NetworkServiceInProcess,LoadCryptoTokenExtension,PermuteTLSExtensions",
        "--disable-features=FlashDeprecationWarning,EnablePasswordsAccountStorage",
        "--deny-permission-prompts",
        "--disable-gpu",
        "--headless=new",
        "--no-sandbox",
        "--crash-dumps-dir=/tmp",
        "--disable-extensions",
        "--disable-dev-shm-usage",
        "--disable-gpu",
        "--user-data-dir=/home/xtreamcodes/m3u8/~/.config/google-chrome/Default",
        "--remote-debugging-port=9222"  # Changed remote debugging port to 9222
    ]

    for argument in arguments:
        options.set_argument(argument)

    driver = None
    try:
        print("Starting Chromium with the following options:")
        for arg in options.arguments:
            print(arg)

        driver = ChromiumPage(addr_driver_opts=options)

        driver.get('https://thetvapp.to/tv/ae-live-stream/')

        # Pass Cloudflare
        while True:
            pass_cycle(driver)
            try:
                ele = driver.s_ele('xpath://h3')
                if ele.text == "thetvapp.to":
                    break
            except Exception as e:
                print(f"Exception during Cloudflare pass: {e}")
                time.sleep(0.1)

    except Exception as e:
        print(f"Exception during driver initialization or navigation: {e}")

    finally:
        if driver:
            # Print the entire HTML content of the page
            page_source = driver.page_source
            print(page_source)
            driver.quit()

