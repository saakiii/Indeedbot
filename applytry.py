from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
import time
from config import *

options = Options()
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36")

chromedriver_path = "Your-CHROMEDRIVEPATH"
driver = webdriver.Chrome(chromedriver_path, options = options)
driver.get("https://www.indeed.com/account/login")

input("Press Enter when you have successfully logged in and searched for a job title:\n")

total_results = driver.find_element(By.CLASS_NAME, "jobsearch-JobCountAndSortPane-jobCount")
total_results_int = int(total_results.text.split(' ', 1)[0].replace(",", ""))
print(total_results_int, "jobs found in total.")

results = driver.find_elements(By.CSS_SELECTOR, ".mosaic-provider-jobcards .tapItem")
items_per_page = 15
num_pages = total_results_int // items_per_page

def find_element_safe(by, value, retries=3, delay=1):
    for _ in range(retries):
        try:
            return driver.find_element(by, value)
        except:
            time.sleep(delay)
    return None

for p in range(num_pages):
    results = driver.find_elements(By.CSS_SELECTOR, ".mosaic-provider-jobcards .tapItem")

    try:
        for result in results:
            hover = ActionChains(driver).move_to_element(result).click()
            hover.perform()
            time.sleep(load_delay)        
            
            apply_btn = find_element_safe(By.CLASS_NAME, "ia-IndeedApplyButton")
            
            if not apply_btn:
                continue
            
            elif apply_btn.text.lower() == 'apply now':
                apply_btn.click()
                time.sleep(load_delay)
                
                # Operations
                windows = driver.window_handles
                driver.switch_to.window(windows[-1])
                
                # Questionnaire
                for i in range(10):  # increase this if you believe there are more than 10 pages of questionnaire

                    applied_title = find_element_safe(By.CLASS_NAME, "ia-HasApplied-bodyTop")
                    if applied_title and "you've applied to this job" in applied_title.text.lower():
                        driver.close()
                        driver.switch_to.window(windows[0])
                        continue
                    
                    questions_title_el = find_element_safe(By.CLASS_NAME, "ia-BasePage-heading")
                    questions_title = questions_title_el.text.lower() if questions_title_el else ''

                    questions_continue_btn = find_element_safe(By.CSS_SELECTOR, '.css-1gljdq7')
                    qualifications_continue_btn = find_element_safe(By.CSS_SELECTOR, '.css-10w34ze')
                    resume_continue_btn = find_element_safe(By.CSS_SELECTOR, ".css-1gljdq7")
                    experience_continue_btn = find_element_safe(By.CSS_SELECTOR, ".css-1gljdq7")
                    submit_application_btn = find_element_safe(By.CSS_SELECTOR, ".css-njr1op")
                    
                    if 'questions' in questions_title:
                        questions = driver.find_elements(By.CLASS_NAME, "ia-Questions-item")
                        for question in questions:
                            question_text = question.find_element(By.CSS_SELECTOR, ".css-kyg8or").text.lower()
                            
                            if 'experience' in question_text:
                                question.find_element(By.CSS_SELECTOR, '[id^="input-q"]').send_keys(Keys.CONTROL, "a", Keys.DELETE)
                                question.find_element(By.CSS_SELECTOR, '[id^="input-q"]').send_keys(add_default_experience)

                            elif 'python experience' in question_text.lower():
                                question.find_element(By.CSS_SELECTOR, '[id^="input-q"]').send_keys(Keys.CONTROL, "a", Keys.DELETE)
                                question.find_element(By.CSS_SELECTOR, '[id^="input-q"]').send_keys(add_python)

                            elif 'javascript experience' in question_text.lower():
                                question.find_element(By.CSS_SELECTOR, '[id^="input-q"]').send_keys(Keys.CONTROL, "a", Keys.DELETE)
                                question.find_element(By.CSS_SELECTOR, '[id^="input-q"]').send_keys(add_javascript)

                            elif 'analysis experience' in question_text.lower():
                                question.find_element(By.CSS_SELECTOR, '[id^="input-q"]').send_keys(Keys.CONTROL, "a", Keys.DELETE)
                                question.find_element(By.CSS_SELECTOR, '[id^="input-q"]').send_keys(add_analysis)

                            elif 'phone' in question_text.lower():
                                question.find_element(By.CSS_SELECTOR, '[id^="input-q"]').send_keys(Keys.CONTROL, "a", Keys.DELETE)
                                question.find_element(By.CSS_SELECTOR, '[id^="input-q"]').send_keys(add_phone)
                                
                            elif 'address' in question_text.lower():
                                question.find_element(By.CSS_SELECTOR, '[id^="input-q"]').send_keys(Keys.CONTROL, "a", Keys.DELETE)
                                question.find_element(By.CSS_SELECTOR, '[id^="input-q"]').send_keys(add_address)
                                
                            elif 'city' in question_text.lower():
                                question.find_element(By.CSS_SELECTOR, '[id^="input-q"]').send_keys(Keys.CONTROL, "a", Keys.DELETE)
                                question.find_element(By.CSS_SELECTOR, '[id^="input-q"]').send_keys(add_city)
                                
                            elif 'github url' in question_text.lower():
                                question.find_element(By.CSS_SELECTOR, '[id^="input-q"]').send_keys(Keys.CONTROL, "a", Keys.DELETE)
                                question.find_element(By.CSS_SELECTOR, '[id^="input-q"]').send_keys(add_github)
                                
                            elif 'teaching experience' in question_text.lower():
                                question.find_element(By.CSS_SELECTOR, '[id^="input-q"]').send_keys(Keys.CONTROL, "a", Keys.DELETE)
                                question.find_element(By.CSS_SELECTOR, '[id^="input-q"]').send_keys(add_teaching)
                                
                            elif 'aws experience' in question_text.lower():
                                question.find_element(By.CSS_SELECTOR, '[id^="input-q"]').send_keys(Keys.CONTROL, "a", Keys.DELETE)
                                question.find_element(By.CSS_SELECTOR, '[id^="input-q"]').send_keys(add_aws)
                                
                            elif 'django experience' in question_text.lower() or 'selenium experience' in question_text.lower():
                                question.find_element(By.CSS_SELECTOR, '[id^="input-q"]').send_keys(Keys.CONTROL, "a", Keys.DELETE)
                                question.find_element(By.CSS_SELECTOR, '[id^="input-q"]').send_keys(add_django)
                                
                            elif 'leadership experience' in question_text.lower():
                                question.find_element(By.CSS_SELECTOR, '[id^="input-q"]').send_keys(Keys.CONTROL, "a", Keys.DELETE)
                                question.find_element(By.CSS_SELECTOR, '[id^="input-q"]').send_keys(add_leadershipdevelopment)
                                
                            elif 'programming experience' in question_text.lower():
                                question.find_element(By.CSS_SELECTOR, '[id^="input-q"]').send_keys(Keys.CONTROL, "a", Keys.DELETE)
                                question.find_element(By.CSS_SELECTOR, '[id^="input-q"]').send_keys(add_programming)
                                
                            elif 'salary' in question_text.lower():
                                question.find_element(By.CSS_SELECTOR, '[id^="input-q"]').send_keys(Keys.CONTROL, "a", Keys.DELETE)
                                question.find_element(By.CSS_SELECTOR, '[id^="input-q"]').send_keys(add_salary)
                                
                            elif 'gender' in question_text.lower():
                                question.find_element(By.CSS_SELECTOR, '[id^="input-q"]').send_keys(Keys.CONTROL, "a", Keys.DELETE)
                                question.find_element(By.CSS_SELECTOR, '[id^="input-q"]').send_keys(add_gender)
                                
                            elif 'postal' in question_text.lower() or 'zip' in question_text.lower():
                                question.find_element(By.CSS_SELECTOR, '[id^="input-q"]').send_keys(Keys.CONTROL, "a", Keys.DELETE)
                                question.find_element(By.CSS_SELECTOR, '[id^="input-q"]').send_keys(add_postal)
                                
                            elif 'state' in question_text.lower():
                                question.find_element(By.CSS_SELECTOR, '[id^="input-q"]').send_keys(Keys.CONTROL, "a", Keys.DELETE)
                                question.find_element(By.CSS_SELECTOR, '[id^="input-q"]').send_keys(add_state)
                                
                            elif 'linkedin url' in question_text.lower():
                                question.find_element(By.CSS_SELECTOR, '[id^="input-q"]').send_keys(Keys.CONTROL, "a", Keys.DELETE)
                                question.find_element(By.CSS_SELECTOR, '[id^="input-q"]').send_keys(add_linkedin)

                            elif 'college' in question_text.lower():
                                question.find_element(By.CSS_SELECTOR, '[id^="input-q"]').send_keys(Keys.CONTROL, "a", Keys.DELETE)
                                question.find_element(By.CSS_SELECTOR, '[id^="input-q"]').send_keys(add_university)

                            elif 'java experience' in question_text.lower():
                                question.find_element(By.CSS_SELECTOR, '[id^="input-q"]').send_keys(Keys.CONTROL, "a", Keys.DELETE)
                                question.find_element(By.CSS_SELECTOR, '[id^="input-q"]').send_keys(add_java)

                            elif 'city' in question_text.lower():
                                question.find_element(By.CSS_SELECTOR, '[id^="input-q"]').send_keys(Keys.CONTROL, "a", Keys.DELETE)
                                question.find_element(By.CSS_SELECTOR, '[id^="input-q"]').send_keys(add_city)
                                
                            elif 'interview' in question_text.lower():
                                question.find_element(By.CSS_SELECTOR, '[id^="input-q"]').send_keys(Keys.CONTROL, "a", Keys.DELETE)
                                question.find_element(By.CSS_SELECTOR, '[id^="input-q"]').send_keys(add_interview_dates)
                            
                            elif 'available to work the following hours' in question_text.lower():
                                question.find_element(By.CSS_SELECTOR, '[id^="input-q"]').send_keys(Keys.CONTROL, "a", Keys.DELETE)
                                question.find_element(By.CSS_SELECTOR, '[id^="input-q"]').send_keys(add_available)
                                
                            elif 'authorization' in question_text.lower() or \
                                'authorized' in question_text.lower() or \
                                'authorized to work' in question_text.lower() or \
                                'authorisation' in question_text.lower() or \
                                'authorised' in question_text.lower() or \
                                'right to work' in question_text.lower() or \
                                'authorised to work' in question_text.lower():
                                question.find_element(By.XPATH, f'//*[contains(text(), "{add_workauthorized}")]').click()
                                
                            elif 'level of education' in question_text.lower():
                                question.find_element(By.XPATH, f'//*[contains(text(), "{add_education}")]').click()
                                
                            elif 'sponsorship' in question_text.lower():
                                question.find_element(By.XPATH, f'//*[contains(text(), "{add_sponsorship}")]').click()
                                
                            elif 'commute' in question_text.lower() or 'travel' in question_text.lower():
                                try:
                                    question.find_element(By.XPATH, f'//*[contains(text(), "{add_commute}")]').click()
                                except:
                                    question.find_element(By.XPATH, f'//*[contains(text(), "{add_commute2}")]').click()
                                
                            elif 'shift' in question_text.lower() or 'travel' in question_text.lower():
                                question.find_element(By.XPATH, f'//*[contains(text(), "{add_shift}")]').click()
                                
                            elif 'veteran' in question_text.lower() or 'disability' in question_text.lower():
                                question.find_element(By.XPATH, f'//*[contains(text(), "{add_disability}")]').click()
                                
                            elif 'DBS' in question_text.lower():
                                question.find_element(By.XPATH, f'//*[contains(text(), "{add_DBS}")]').click()
                                
                            elif 'criminal' in question_text.lower():
                                try:
                                    question.find_element(By.XPATH, f'//*[contains(text(), "{add_criminal}")]').click()
                                except:
                                    question.find_elements(By.XPATH, f'//span[contains(text(), "{add_criminal}")]')[-1].click()
                                
                            elif 'valid' in question_text.lower():
                                question.find_element(By.XPATH, f'//*[contains(text(), "{add_valid_cert}")]').click()
                                
                            elif 'gender' in question_text.lower():
                                question.find_element(By.XPATH, f'//*[contains(text(), "{add_gender}")]').click()
                                
                            elif 'hear about this position' in question_text.lower():
                                question.find_element(By.XPATH, f'//*[contains(text(), "{add_disability}")]').click()
                                
                            else:
                                unknown_multi_questions = find_element_safe(By.CSS_SELECTOR, 'css-14vzfv5')
                                unknown_written_question = find_element_safe(By.CSS_SELECTOR, '[id^="input-q"]')
                                
                                if unknown_written_question:
                                    unknown_written_question.send_keys(add_default_experience)
                                if unknown_multi_questions:
                                    question.find_element(By.XPATH, f'//*[contains(text(), "{default_unknown_multi}")]').click()

                    # clicks the submit or contiune btn
                    if questions_continue_btn:
                        questions_continue_btn.click()
                        time.sleep(load_delay)
                    elif qualifications_continue_btn:
                        qualifications_continue_btn.click()
                        time.sleep(load_delay)
                    elif resume_continue_btn:
                        resume_continue_btn.click()
                        time.sleep(load_delay)
                    elif experience_continue_btn:
                        experience_continue_btn.click()
                        time.sleep(load_delay)
                    elif submit_application_btn:
                        submit_application_btn.click()
                        time.sleep(load_delay)
                        break

                    else:
                        print("There appears to be something wrong with this job. Skipping.")
                        break

                driver.close()
                driver.switch_to.window(windows[0])
    except Exception as e:
        print(f"Error: {e}")
        windows = driver.window_handles
        driver.switch_to.window(windows[0])
        driver.refresh()
        continue
    
    while True:
        try:
            driver.find_element(By.XPATH, "//a[@data-testid='pagination-page-next']").click()
            break
        except Exception as e:
            print(f"Pagination error: {e}")
            driver.refresh()
            time.sleep(load_delay)
    
    time.sleep(load_delay)
