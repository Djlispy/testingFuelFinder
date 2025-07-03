from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import json
import urllib

def main():
    display = Display(visible=0, size=(1920, 1080))
    display.start()

    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    # Do NOT add --headless here if using pyvirtualdisplay

    driver = webdriver.Chrome(options=chrome_options)

    driver.get("https://www.7-eleven.com/locator")
    time.sleep(3)  # allow site to fully load and generate cookies

    cookies = driver.get_cookies()

    auth_token = None
    for cookie in cookies:
        if cookie['name'] == 'sei-rewards-tokens':
            auth_token = cookie['value']
            break

    if auth_token:
        print("✅ Token found in cookie:")
        decoded = urllib.parse.unquote(auth_token)
        data = json.loads(decoded)
        bearer_token = "Bearer " + data.get("access_token", "")
        print(bearer_token)
    else:
        print("❌ Token cookie not found.")

    driver.quit()
    display.stop()

if __name__ == "__main__":
    main()
