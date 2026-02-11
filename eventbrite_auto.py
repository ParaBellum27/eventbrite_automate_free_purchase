from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time

# ===== CONFIGURATION - CHANGE THESE VALUES =====
FIRST_NAME = "Jean"
LAST_NAME = "Gabriel"
EMAIL = "pg2576@stern.nyu.edu"
EVENTBRITE_URL = ""  # Leave empty for manual navigation, or paste event URL here
# ===============================================

def find_element_by_multiple_selectors(driver, wait, selectors):
    """Try multiple selectors until one works"""
    for selector_type, selector_value in selectors:
        try:
            if selector_type == "id":
                element = wait.until(EC.presence_of_element_located((By.ID, selector_value)))
            elif selector_type == "name":
                element = wait.until(EC.presence_of_element_located((By.NAME, selector_value)))
            elif selector_type == "css":
                element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selector_value)))
            elif selector_type == "xpath":
                element = wait.until(EC.presence_of_element_located((By.XPATH, selector_value)))
            return element
        except (TimeoutException, NoSuchElementException):
            continue
    return None

def automate_eventbrite_registration():
    print("🚀 Starting Eventbrite Auto-Registration...")
    print(f"📋 Will fill: {FIRST_NAME} {LAST_NAME}, {EMAIL}")
    
    # Set up Chrome with options for speed
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")  # Avoid detection
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    driver = webdriver.Chrome(options=chrome_options)
    driver.maximize_window()
    
    wait = WebDriverWait(driver, 15)
    
    try:
        # Navigate to URL if provided
        if EVENTBRITE_URL:
            print(f"🌐 Navigating to: {EVENTBRITE_URL}")
            driver.get(EVENTBRITE_URL)
            print("⏳ Waiting for you to:")
            print("   1. Click 'Get tickets'")
            print("   2. Select quantity")
            print("   3. Click 'Check out'")
            input("\n▶️  Press ENTER when you're on the CHECKOUT page...")
        else:
            print("\n⏳ Waiting for you to navigate to the Eventbrite event page...")
            print("👉 Steps:")
            print("   1. Open the event link in Chrome")
            print("   2. Click 'Get tickets'")
            print("   3. Select quantity (1 ticket)")
            print("   4. Click 'Check out'")
            input("\n▶️  Press ENTER when you're on the CHECKOUT page (with the form)...")
        
        print("\n🔍 Detecting form fields...")
        
        # Multiple selectors for First Name field (try all variations)
        first_name_selectors = [
            ("id", "first-name"),
            ("id", "firstName"),
            ("name", "first_name"),
            ("name", "firstName"),
            ("css", "input[placeholder*='First' i]"),
            ("css", "input[placeholder*='Prénom' i]"),  # French
            ("xpath", "//input[contains(@id, 'first') or contains(@name, 'first')]")
        ]
        
        # Multiple selectors for Last Name field
        last_name_selectors = [
            ("id", "last-name"),
            ("id", "lastName"),
            ("name", "last_name"),
            ("name", "lastName"),
            ("css", "input[placeholder*='Last' i]"),
            ("css", "input[placeholder*='Nom' i]"),  # French
            ("xpath", "//input[contains(@id, 'last') or contains(@name, 'last')]")
        ]
        
        # Multiple selectors for Email field
        email_selectors = [
            ("id", "email"),
            ("name", "email"),
            ("css", "input[type='email']"),
            ("css", "input[placeholder*='Email' i]"),
            ("xpath", "//input[@type='email' or contains(@name, 'email')]")
        ]
        
        # Find and fill First Name
        print(f"✍️  Filling First Name: {FIRST_NAME}")
        first_name = find_element_by_multiple_selectors(driver, wait, first_name_selectors)
        if first_name:
            first_name.clear()
            time.sleep(0.1)
            first_name.send_keys(FIRST_NAME)
            print("   ✅ First name filled")
        else:
            print("   ⚠️  Could not find first name field - will proceed anyway")
        
        # Find and fill Last Name
        print(f"✍️  Filling Last Name: {LAST_NAME}")
        last_name = find_element_by_multiple_selectors(driver, wait, last_name_selectors)
        if last_name:
            last_name.clear()
            time.sleep(0.1)
            last_name.send_keys(LAST_NAME)
            print("   ✅ Last name filled")
        else:
            print("   ⚠️  Could not find last name field - will proceed anyway")
        
        # Find and fill Email
        print(f"✍️  Verifying Email: {EMAIL}")
        email_field = find_element_by_multiple_selectors(driver, wait, email_selectors)
        if email_field:
            email_field.clear()
            time.sleep(0.1)
            email_field.send_keys(EMAIL)
            print("   ✅ Email filled")
        else:
            print("   ⚠️  Could not find email field - will proceed anyway")
        
        print("\n✅ All fields filled!")
        print("⏱️  Waiting 0.5 seconds before submitting...")
        time.sleep(0.5)
        
        # Find and click submit button (multiple variations)
        submit_button_selectors = [
            ("css", "button[type='submit']"),
            ("xpath", "//button[contains(text(), 'Place Order')]"),
            ("xpath", "//button[contains(text(), 'Register')]"),
            ("xpath", "//button[contains(text(), 'Check out')]"),
            ("xpath", "//button[contains(text(), 'Complete')]"),
            ("css", ".eds-btn--button"),
            ("css", "button.eds-btn--primary")
        ]
        
        print("🎯 Looking for submit button...")
        submit_button = None
        for selector_type, selector_value in submit_button_selectors:
            try:
                if selector_type == "css":
                    submit_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector_value)))
                elif selector_type == "xpath":
                    submit_button = wait.until(EC.element_to_be_clickable((By.XPATH, selector_value)))
                print("   ✅ Found submit button!")
                break
            except (TimeoutException, NoSuchElementException):
                continue
        
        if submit_button:
            submit_button.click()
            print("\n🎉 SUCCESS! Order submitted!")
            print(f"📧 Check {EMAIL} for confirmation")
            time.sleep(5)
        else:
            print("\n⚠️  Could not find submit button automatically")
            print("👉 Please click the submit button manually")
            input("Press ENTER after you've submitted...")
        
    except Exception as e:
        print(f"\n❌ Error occurred: {str(e)}")
        print("💡 The browser will stay open so you can manually complete it")
        input("Press ENTER to close the browser...")
    
    finally:
        print("\n👋 Closing browser in 3 seconds...")
        time.sleep(3)
        driver.quit()

if __name__ == "__main__":
    automate_eventbrite_registration()