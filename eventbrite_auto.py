#!/usr/bin/env python3
"""
Eventbrite Ticket Monitor & Auto-Booker
Checks every 3 minutes if tickets become available and automatically books them
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import os
from datetime import datetime

# ===== CONFIGURATION =====
EVENTBRITE_URL = "https://www.eventbrite.com/e/reception-en-presence-du-createur-valerian-hughes-i-grand-public-tickets-1982713913689"
CHECK_INTERVAL = 180  # 3 minutes in seconds
FIRST_NAME = "X"
LAST_NAME = "Y"
EMAIL = "pg2576@stern.nyu.edu"
# =========================

def log(message):
    """Print message with timestamp"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")

def check_availability(driver):
    """Check if tickets are available (not sold out)"""
    try:
        # Look for "Sold out" text
        sold_out_indicators = [
            "sold out",
            "tickets are no longer available",
            "registration is closed",
            "event is sold out"
        ]
        
        page_text = driver.page_source.lower()
        
        for indicator in sold_out_indicators:
            if indicator in page_text:
                return False
        
        # Look for "Get tickets" or "Register" button
        try:
            get_tickets_button = driver.find_element(By.XPATH, 
                "//button[contains(text(), 'Get tickets') or contains(text(), 'Register') or contains(text(), 'Checkout')]")
            return True
        except NoSuchElementException:
            pass
        
        # If we can't find sold out text and there's a tickets button, assume available
        return True
        
    except Exception as e:
        log(f"Error checking availability: {e}")
        return False

def fill_form_and_submit(driver):
    """Fill out the checkout form and submit"""
    wait = WebDriverWait(driver, 15)
    
    log("🔍 Looking for form fields...")
    
    # Wait a moment for page to settle
    time.sleep(2)
    
    # Multiple selectors for first name
    first_name_selectors = [
        ('css', 'input[id="buyer.N-first_name"]'),
        ('css', 'input[name="buyer.N-first_name"]'),
        ('css', 'input[placeholder*="First" i]'),
        ('css', 'input[autocomplete="given-name"]')
    ]
    
    # Multiple selectors for last name
    last_name_selectors = [
        ('css', 'input[id="buyer.N-last_name"]'),
        ('css', 'input[name="buyer.N-last_name"]'),
        ('css', 'input[placeholder*="Last" i]'),
        ('css', 'input[autocomplete="family-name"]')
    ]
    
    # Multiple selectors for email
    email_selectors = [
        ('css', 'input[id="buyer.N-email"]'),
        ('css', 'input[name="buyer.N-email"]'),
        ('css', 'input[type="email"]')
    ]
    
    def find_and_fill(selectors, value, field_name):
        for selector_type, selector in selectors:
            try:
                field = driver.find_element(By.CSS_SELECTOR, selector)
                field.clear()
                field.send_keys(value)
                log(f"✅ Filled {field_name}: {value}")
                return True
            except:
                continue
        log(f"⚠️  Could not find {field_name} field")
        return False
    
    # Fill all fields
    find_and_fill(first_name_selectors, FIRST_NAME, "First Name")
    time.sleep(0.2)
    find_and_fill(last_name_selectors, LAST_NAME, "Last Name")
    time.sleep(0.2)
    find_and_fill(email_selectors, EMAIL, "Email")
    
    log("⏱️  Waiting 1 second before submitting...")
    time.sleep(1)
    
    # Find and click submit button
    submit_selectors = [
        "//button[contains(text(), 'Register')]",
        "//button[contains(text(), 'Place Order')]",
        "//button[@type='submit']",
        "//button[contains(text(), 'Complete')]"
    ]
    
    for selector in submit_selectors:
        try:
            button = driver.find_element(By.XPATH, selector)
            button.click()
            log("🎉 FORM SUBMITTED!")
            return True
        except:
            continue
    
    log("⚠️  Could not find submit button - form may need manual submission")
    return False

def book_ticket(driver):
    """Navigate through booking flow and complete purchase"""
    try:
        log("🎟️  TICKETS AVAILABLE! Starting booking process...")
        
        # Click "Get tickets" button
        wait = WebDriverWait(driver, 10)
        
        # Try different button texts
        button_texts = ["Get tickets", "Register", "Select tickets"]
        for text in button_texts:
            try:
                button = wait.until(EC.element_to_be_clickable(
                    (By.XPATH, f"//button[contains(text(), '{text}')]")
                ))
                button.click()
                log(f"✅ Clicked '{text}' button")
                break
            except:
                continue
        
        time.sleep(2)
        
        # Select quantity (1 ticket)
        try:
            # Look for quantity selector
            quantity_input = driver.find_element(By.CSS_SELECTOR, 
                "input[type='number'], select[name*='quantity']")
            quantity_input.clear()
            quantity_input.send_keys("1")
            log("✅ Selected 1 ticket")
        except:
            log("ℹ️  Quantity already set or not needed")
        
        time.sleep(1)
        
        # Click "Checkout" button
        try:
            checkout_button = wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(text(), 'Checkout') or contains(text(), 'Check out')]")
            ))
            checkout_button.click()
            log("✅ Clicked Checkout button")
        except:
            log("⚠️  Could not find Checkout button")
        
        time.sleep(3)
        
        # Fill form and submit
        fill_form_and_submit(driver)
        
        log("🎊 BOOKING COMPLETE! Check your email for confirmation.")
        return True
        
    except Exception as e:
        log(f"❌ Error during booking: {e}")
        return False

def monitor_event():
    """Main monitoring loop"""
    log("🚀 Starting Eventbrite Monitor...")
    log(f"📋 Target: {EVENTBRITE_URL}")
    log(f"🕐 Check interval: {CHECK_INTERVAL} seconds (3 minutes)")
    log(f"👤 Booking as: {FIRST_NAME} {LAST_NAME} ({EMAIL})")
    log("=" * 60)
    
    # Set up Chrome - just opens a new window/tab
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    
    log("\n🌐 Opening Chrome browser...")
    log("ℹ️  A new Chrome window will open")
    log("ℹ️  You can keep your other Chrome windows open!")
    
    driver = webdriver.Chrome(options=chrome_options)
    driver.maximize_window()
    
    # First, go to Eventbrite and let user log in
    log("\n⚠️  FIRST TIME SETUP:")
    log("   The browser will open Eventbrite")
    log("   Please LOG IN to your Eventbrite account (pg2576@stern.nyu.edu)")
    log("   (This login will persist for the monitoring session)")
    
    driver.get("https://www.eventbrite.com/signin/")
    log("\n👉 Please log in to Eventbrite in the opened browser...")
    input("▶️  Press ENTER after you've logged in...")
    
    log("\n✅ Great! Now monitoring will begin...")
    log("=" * 60)
    driver.maximize_window()
    
    check_count = 0
    
    try:
        while True:
            check_count += 1
            log(f"🔍 Check #{check_count}: Loading event page...")
            
            try:
                driver.get(EVENTBRITE_URL)
                time.sleep(3)  # Wait for page to load
                
                if check_availability(driver):
                    log("✅ TICKETS AVAILABLE!")
                    log("🎯 Attempting to book...")
                    
                    if book_ticket(driver):
                        log("=" * 60)
                        log("🎉 SUCCESS! Ticket booking completed!")
                        log(f"📧 Confirmation should be sent to: {EMAIL}")
                        log("=" * 60)
                        break
                    else:
                        log("⚠️  Booking failed, will retry on next check")
                else:
                    log("❌ Still sold out")
                
            except Exception as e:
                log(f"❌ Error during check: {e}")
            
            # Wait before next check
            if check_count < 999:  # Continue monitoring
                log(f"⏰ Next check in {CHECK_INTERVAL} seconds ({CHECK_INTERVAL//60} minutes)...")
                log("-" * 60)
                time.sleep(CHECK_INTERVAL)
            else:
                break
    
    except KeyboardInterrupt:
        log("\n⚠️  Monitoring stopped by user")
    
    finally:
        log("👋 Closing browser...")
        time.sleep(3)
        driver.quit()

    monitor_event()
if __name__ == "__main__":