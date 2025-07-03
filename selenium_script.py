from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from pyvirtualdisplay import Display
import time
import json
import urllib

display = Display(visible=0, size=(1920, 1080))
display.start()

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1280,1024")

driver = webdriver.Chrome(options=chrome_options)

driver.get("https://www.7-eleven.com/locator")
time.sleep(2)

cookies = driver.get_cookies()

# Find the sei-rewards-tokens cookie
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
