from pyvirtualdisplay import Display
import undetected_chromedriver as uc
import time, json, urllib

display = Display(visible=0, size=(1920, 1080))
display.start()

options = uc.ChromeOptions()
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--window-size=1920,1080")
# Do NOT add --headless here — UC uses its own stealth headless mode

driver = uc.Chrome(options=options)

driver.get("https://www.7-eleven.com/locator")
time.sleep(10)  # Increase wait to give page time to finish dynamic JS

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
    print("✅ Token found:")
    decoded = urllib.parse.unquote(auth_token)
    data = json.loads(decoded)
    bearer_token = "Bearer " + data.get("access_token", "")
    print(bearer_token)
else:
    print("❌ Token cookie not found.")

driver.quit()
display.stop()
