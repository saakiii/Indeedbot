import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config_ind import (
    search_keyword,
    search_location,
    job_type,
    salary_range,
    experience_level,
    remote_option,
    company_rating,
    date_posted,
)
from details import DETAILS

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

# Generate Indeed URL with Filters
def generate_indeed_url():
    base_url = "https://www.indeed.com/jobs"
    params = {
        "q": search_keyword.replace(" ", "+"),
        "l": search_location.replace(" ", "+"),
        "jt": job_type,
        "salary": salary_range.replace("+", "%2B"),
        "explvl": experience_level,
        "remote": remote_option,
        "fromage": date_posted,
        "rating": company_rating,
    }
    query_params = "&".join([f"{key}={value}" for key, value in params.items() if value])
    full_url = f"{base_url}?{query_params}"
    print(f"Generated URL: {full_url}")
    return full_url

#handling Job
def handle_job_application(driver):
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

                    # Locate and click the "Apply now" button in the left side panel
                    try:
                        apply_button = WebDriverWait(driver, 10).until(
                            EC.element_to_be_clickable((By.ID, "indeedApplyButton"))
                        )
                        apply_button.click()
                        print("'Apply now' button clicked.")
                        time.sleep(2)
                    except Exception as e:
                        print(f"Error clicking 'Apply now' button: {e}")
                        continue
                    
                    # Switch to the new tab opened by Indeed
                    driver.switch_to.window(driver.window_handles[-1])
                    print("Switched to the new tab.")
                    
                    # If "Continue applying" button exists, click it
                    try:
                        continue_applying_button = WebDriverWait(driver, 5).until(
                            EC.element_to_be_clickable((By.XPATH, "//button/span[text()='Continue applying']"))
                        )
                        continue_applying_button.click()
                        print("Clicked 'Continue applying' to proceed to resume handling.")
                        time.sleep(2)
                    except:
                        print("No 'Continue applying' button found. Proceeding to resume handling.")
                    
                    # Handle resume upload/selection
                    handle_resume_page(driver)
                    
                    # Exit after applying to one job
                    return True
            
            except Exception as e:
                print(f"Skipping job: {e}")
                continue
                
        print("No more 'Easily apply' jobs found.")
        return False
    
    except Exception as e:
        print(f"Error finding 'Easily apply' jobs: {e}")
        return False

# Handle Resume Page
# Handle Resume Page (after "Apply now" and new tab opens)
def handle_resume_page(driver):
    try:
        print("Handling resume page...")
        time.sleep(2)  # Allow page to load

        # If "Continue applying" button exists, click it
        try:
            continue_button = WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable((By.XPATH, "//button/span[text()='Continue applying']"))
            )
            continue_button.click()
            print("'Continue applying' button clicked.")
            time.sleep(2)
        except:
            print("No 'Continue applying' button found. Proceeding to resume selection.")

        # Select the pre-uploaded resume option
        resume_radio = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input[data-testid='FileResumeCard-input']"))
        )
        resume_radio.click()
        print("Selected pre-uploaded resume.")

        # Click "Continue" to proceed
        continue_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button/span[text()='Continue']"))
        )
        continue_button.click()
        print("Clicked 'Continue' to proceed.")

    except Exception as e:
        print(f"Error handling resume page: {e}")

# Main Function
def main():
    # Launch browser
    driver = setup_driver()
    
    # Open Indeed login page
    driver.get("https://www.indeed.com/account/login")
    print("Navigate to the Indeed login page and log in manually.")
    input("Press Enter after you have logged in...\n")
    
    # Generate URL using config_ind.py values
    search_url = generate_indeed_url()
    
    # Navigate to job search page
    driver.get(search_url)
    print(f"Navigating to: {search_url}")
    time.sleep(5)  # Wait for the page to load
    
    # Process job application
    if not handle_job_application(driver):
        print("No valid 'Easy Apply' jobs found.")
    
    # Keep the tab open for debugging
    print("Job application process completed. Keeping the browser open.")
    input("Press Enter to close the browser...\n")
    
    # Close browser
    driver.quit()
    print("Browser closed.")

if __name__ == "__main__":
    main()
