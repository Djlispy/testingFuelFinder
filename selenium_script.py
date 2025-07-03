from pyvirtualdisplay import Display
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time, json, urllib

display = Display(visible=0, size=(1920, 1080))
display.start()

options = uc.ChromeOptions()
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--window-size=1920,1080")

driver = uc.Chrome(options=options)

driver.get("https://www.7-eleven.com/locator")

try:
    # 1. Wait for the ZIP input and type ZIP code
    zip_input = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.ID, "form_location"))
    )
    zip_input.clear()
    zip_input.send_keys("35679")
    print("✅ Entered ZIP code")

    # 2. Wait for the Search button
    search_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "input[type='submit'][value='Search']"))
    )

    # Scroll to the button
    driver.execute_script("arguments[0].scrollIntoView(true);", search_button)
    time.sleep(1)

    # Click the Search button via JS to avoid hover-only issues
    driver.execute_script("arguments[0].click();", search_button)
    print("✅ Clicked Search button")

except Exception as e:
    print(f"❌ ZIP/Search interaction failed: {e}")

# 3. Wait for token generation after interaction
time.sleep(6)

# 4. Take a screenshot to debug visual state
driver.save_screenshot("page.png")

# 5. Dump localStorage
local_storage = driver.execute_script("return window.localStorage;")
print("\n📦 Local Storage:")
for k, v in local_storage.items():
    print(f"{k}: {v}")

# 6. Dump sessionStorage
session_storage = driver.execute_script("return window.sessionStorage;")
print("\n📦 Session Storage:")
for k, v in session_storage.items():
    print(f"{k}: {v}")

# 7. Dump cookies and search for token cookie
cookies = driver.get_cookies()
auth_token = None
print("\n🍪 Cookies:")
for cookie in cookies:
    print(f"{cookie['name']} = {cookie['value']}")
    if cookie['name'] == 'sei-rewards-tokens':
        auth_token = cookie['value']

# 8. Decode and print token if found
if auth_token:
    print("\n✅ Token found in cookie:")
    decoded = urllib.parse.unquote(auth_token)
    data = json.loads(decoded)
    bearer_token = "Bearer " + data.get("access_token", "")
    print(bearer_token)
else:
    print("\n❌ Token cookie not found.")

driver.quit()
display.stop()
