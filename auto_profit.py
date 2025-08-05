from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import os
import time
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Environment variables
USERNAME = os.getenv("USERNAME", "8308761179")
PASSWORD = os.getenv("PASSWORD", "harshal123")

LOGIN_URL = "https://www.hpintfinance.com/index/login/index.html"
EARNINGS_URL = "https://www.hpintfinance.com/index/index/earnings.html"

def setup_driver():
    chrome_options = Options()
    
    # Headless mode (new recommended flag)
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920x1080")
    
    # Disable unnecessary features
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-application-cache")
    
    # Manually specify Chrome binary location (for Codespaces)
    chrome_options.binary_location = "/usr/bin/google-chrome"
    
    # Force WebDriver Manager to use latest ChromeDriver
    service = Service(ChromeDriverManager().install())
    
    return webdriver.Chrome(service=service, options=chrome_options)

def run():
    driver = None
    try:
        driver = setup_driver()
        wait = WebDriverWait(driver, 20)
        
        # Step 1: Login
        logging.info("🌐 Navigating to login page...")
        driver.get(LOGIN_URL)
        time.sleep(2)

        logging.info("🔑 Logging in...")
        wait.until(EC.presence_of_element_located((By.ID, "phone"))).send_keys(USERNAME)
        driver.find_element(By.ID, "password").send_keys(PASSWORD)
        driver.find_element(By.CLASS_NAME, "login").click()
        time.sleep(3)

        # Step 2: Earnings page
        logging.info("💵 Navigating to earnings page...")
        driver.get(EARNINGS_URL)
        time.sleep(3)

        # Step 3: Click "Get it now" button
        logging.info("🔄 Attempting to click button...")
        try:
            button = wait.until(EC.element_to_be_clickable((By.ID, "btna1")))
            button.click()
            logging.info("✅ Successfully clicked button!")
            time.sleep(3)
        except Exception as e:
            logging.error(f"⚠️ Button click failed: {str(e)}")
            try:
                driver.execute_script("document.getElementById('btna1').click()")
                logging.info("✅ Clicked using JavaScript fallback!")
            except Exception as js_e:
                logging.error(f"⚠️ JavaScript click failed: {str(js_e)}")
                driver.save_screenshot("error.png")
                logging.info("📸 Saved screenshot as 'error.png'")

        logging.info("🏁 Script completed successfully!")

    except Exception as e:
        logging.error(f"❌ Fatal error: {str(e)}")
        if driver:
            driver.save_screenshot("fatal_error.png")
            logging.info("📸 Saved fatal error screenshot")
    finally:
        if driver:
            driver.quit()
            logging.info("🧹 Cleaned up browser instance")

if __name__ == "__main__":
    run()