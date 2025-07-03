from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import json
import urllib

def main():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1280,1024")
    
    driver = webdriver.Chrome(options=chrome_options)
    
    driver.get("https://www.7-eleven.com/locator")
    time.sleep(3)  # wait for page load
    
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

if __name__ == "__main__":
    main()
