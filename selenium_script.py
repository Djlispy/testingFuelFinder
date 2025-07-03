from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import json
import urllib
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def main():
    display = Display(visible=0, size=(1920, 1080))
    display.start()

    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36")

    # Do NOT add --headless here if using pyvirtualdisplay

    driver = webdriver.Chrome(options=chrome_options)

    driver.get("https://www.7-eleven.com/locator")
    try:
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.ID, "panel-map"))
        )
    except:
        print("⚠️ Timeout waiting for page")

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    time.sleep(15)  # allow site to fully load and generate cookies


    cookies = driver.get_cookies()
    print("All cookies:")
    for cookie in cookies:
        print(cookie['name'])

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
