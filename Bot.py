import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ChromeDriver Path
chromedriver_path = "/Users/saakin/Downloads/chromedriver-mac-arm64/chromedriver"

# Configure Chrome Options
options = Options()
options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.6943.54 Safari/537.36"
)
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)
options.add_argument("--start-maximized")

# Initialize WebDriver
def setup_driver():
    try:
        print("Launching browser...")
        driver = webdriver.Chrome(service=Service(chromedriver_path), options=options)
        print("Browser launched successfully.")
        return driver
    except Exception as e:
        print(f"Error initializing ChromeDriver: {e}")
        exit()

def switch_to_new_tab(driver):
    """Switch to the newly opened tab"""
    print("Switching to the new tab.")
    driver.switch_to.window(driver.window_handles[-1])

def handle_commute_check(driver):
    """Handle commute check page if it appears"""
    try:
        print("Checking for 'Continue applying' button on commute check page.")
        commute_continue_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".css-kz83v6.e8ju0x50[data-testid='commute-check-continue-button']"))
        )
        # Scroll down to the button to ensure visibility
        driver.execute_script("arguments[0].scrollIntoView(true);", commute_continue_button)
        commute_continue_button.click()
        print("Clicked 'Continue applying' to move past the commute check page.")
        time.sleep(2)  # Give some time for the next page to load
    except:
        print("No commute check page. Proceeding to resume selection.")

def handle_resume_selection(driver):
    """Handle resume page selection"""
    try:
        print("Handling resume page...")
        time.sleep(2)  # Allow page to load
        
        # Select the pre-uploaded resume option (second radio button)
        saved_resume_radio = WebDriverWait(driver, 15).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "input[data-testid='FileResumeCard-input'][value='SAVED_FILE_RESUME']"))
        )
        saved_resume_radio.click()
        print("Selected pre-uploaded resume.")
        time.sleep(3)  # Wait for the resume section to expand
        
        # Click the "Continue" button to proceed
        continue_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button/span[text()='Continue']"))
        )
        continue_button.click()
        print("Clicked 'Continue' to proceed to the next page.")
    except Exception as e:
        print(f"Error handling resume page: {e}")

def handle_job_application(driver):
    """Handle job application process"""
    try:
        print("Searching for 'Easily apply' jobs...")
        
        # Wait for job cards to load
        job_cards = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.job_seen_beacon"))
        )

        for job_card in job_cards:
            try:
                # Check if the job card contains "Easily apply"
                easily_apply_container = job_card.find_elements(
                    By.XPATH, ".//div[contains(@class, 'css-r19t1s')]//span[contains(text(), 'Easily apply')]"
                )
                if easily_apply_container:
                    print("Found 'Easily apply' job. Clicking job card...")
                    
                    # Click the job card container to open the side panel
                    driver.execute_script("arguments[0].scrollIntoView(true);", job_card)
                    job_card.click()
                    time.sleep(2)
                
                    # Locate and click the "Apply now" button on the left side panel
                    try:
                        apply_button = WebDriverWait(driver, 10).until(
                            EC.element_to_be_clickable((By.CSS_SELECTOR, "#indeedApplyButton"))
                        )
                        apply_button.click()
                        print("'Apply now' button clicked.")
                        time.sleep(2)
                    except Exception as e:
                        print(f"Error clicking 'Apply now' button: {e}")
                        continue
                    
                    # Switch to the newly opened tab
                    switch_to_new_tab(driver)
                    
                    # Handle commute check if it appears
                    handle_commute_check(driver)
                    
                    # Handle resume selection
                    handle_resume_selection(driver)
            
            except Exception as e:
                print(f"Error handling job card: {e}")
                continue
    except Exception as e:
        print(f"Error finding 'Easily apply' jobs: {e}")

# Main function to run the automation
def main():
    # Launch browser
    driver = setup_driver()
    
    # Open Indeed login page
    driver.get("https://www.indeed.com/account/login")
    print("Navigate to the Indeed login page and log in manually.")
    input("Press Enter after you have logged in...\n")
    
    # Generate search URL (you can replace this with your desired search parameters)
    search_url = "https://www.indeed.com/jobs?q=Business+Analyst&l=United+States&jt=fulltime&salary=50000%2B&fromage=last_24_hours"
    
    # Navigate to job search page
    driver.get(search_url)
    print(f"Navigating to: {search_url}")
    time.sleep(5)  # Wait for the page to load
    
    # Handle job application
    handle_job_application(driver)
    
    # Keep the tab open for debugging
    print("Job application process completed. Keeping the browser open.")
    input("Press Enter to close the browser...\n")
    
    # Close browser
    driver.quit()
    print("Browser closed.")

if __name__ == "__main__":
    main()
