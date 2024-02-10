from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
import time
from webdriver_manager.chrome import ChromeDriverManager
import updater

def service_and_options(headless = False):
    option = webdriver.ChromeOptions()
    option.add_experimental_option('excludeSwitches', ['enable-logging'])
    if headless:
        option.add_argument('--headless')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=option)
    option.add_experimental_option(
        "prefs", {
            # block image loading
            "profile.managed_default_content_settings.images": 2,
        })
    return driver

def log_in_function(username, password, driver):
    
    try: 
        driver.find_element(By.CSS_SELECTOR, 'input[formcontrolname="userName"]').send_keys(username)
        driver.find_element(By.CSS_SELECTOR, 'input[formcontrolname="password"]').send_keys(password)
        driver.find_element(By.CSS_SELECTOR, 'button[data-qa="button-login"]').click()
        driver.implicitly_wait(10)
    except:
        pass
    
def main():
    
    running = True
    
    while running:
        print("What to do?")
        print("\n1. Open the webpage \n2. Update\n3. Exit")
        
        decision = input("\nSelect 1, 2 or 3: ")
        
        if decision == "1":
            
            driver = service_and_options()
    
            url = "https://www.google.com"
            
            driver.get(url)
            
            for i in range(10):
                time.sleep(1)
                print(10-i)
        
        elif decision == "2":
            
            updater.main()
        
        elif decision == "3":
            running = False
        
        else:
            print("Select 1, 2 or 3 please")
            continue
    
        
        
main()