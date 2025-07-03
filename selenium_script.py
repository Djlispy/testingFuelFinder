from pyvirtualdisplay import Display
import undetected_chromedriver as uc
import time, json, urllib
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

display = Display(visible=0, size=(1920, 1080))
display.start()

options = uc.ChromeOptions()
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--window-size=1920,1080")
# Do NOT add --headless here — UC uses its own stealth headless mode

driver = uc.Chrome(options=options)

driver.get("https://www.7-eleven.com/locator")

try:
    # 1. Type ZIP into input
    zip_input = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.ID, "form_location"))
    )
    zip_input.clear()
    zip_input.send_keys("35679")
    print("✅ Entered ZIP code")

    # 2. Click the Search button
    search_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "input[type='submit'][value='Search']"))
    )
    search_button.click()
    print("✅ Clicked Search button")

except Exception as e:
    print(f"❌ ZIP/Search interaction failed: {e}")

# 3. Wait for JS/XHR to complete
time.sleep(6)

driver.save_screenshot("page.png")


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
