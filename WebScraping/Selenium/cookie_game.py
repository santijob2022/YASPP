import os
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
# If a clickable element is intercepted
from selenium.webdriver.common.action_chains import ActionChains
# Wait for an element to be available
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

load_dotenv()

chrome_driver_path = os.environ["driver_path"]
driver =webdriver.Chrome(executable_path=chrome_driver_path)
driver.get("https://orteil.dashnet.org/cookieclicker/")

##################### Selection language #####################
# wait for the button to become clickable
lang_selection = WebDriverWait(driver, 60).until(
    EC.element_to_be_clickable((By.XPATH, '//*[@id="langSelect-EN"]'))        
)
# create an ActionChains object and move the mouse to the button
actions = ActionChains(driver)

actions.move_to_element(lang_selection)    
actions.click(lang_selection).perform()

##################### Clicking cookies #####################
#bigCookie_button = driver.find_element(By.ID,'bigCookie')

bigCookie_button = WebDriverWait(driver, 60).until(
    EC.element_to_be_clickable((By.ID, 'bigCookie'))        
)

start_time = time.time()
j=1 # Iteration number
while True:
    # To check for new boosts
    if (time.time() - start_time) >j*10:
        print("\n\n\n Iteration: ",j)
        upgrade_buttons = driver.find_elements(By.CSS_SELECTOR,".product.unlocked.enabled")        
        length = len(upgrade_buttons)                               
        if length>0 :            
            cookies = driver.find_element(By.XPATH, '//*[@id="cookies"]').text.split()[0].strip()
            if int(cookies)>105:
                for i in range(length-1,-1,-1):                
                    price = driver.find_element(By.ID, f"productPrice{i}").text
                    print("From bigger to smaller - Price: ",price, ", - item: ",upgrade_buttons[i].text, "Cookies per second: ",cookies)
                    if int(cookies)>=int(price):
                        actions.move_to_element(upgrade_buttons[i])    
                        actions.click(upgrade_buttons[i]).perform()            
            cookies = driver.find_element(By.XPATH, '//*[@id="cookies"]').text.split()[0].strip() # to track cookies after upgrade            
            print("Printing Stuff - ","Length: ",length," Cookies per second: ",cookies,"\n\n\n")                          
        else:
            print("Empty!!!!")
        j+=1    

    # To click the Big cookie button    
    actions.move_to_element(bigCookie_button)
    actions.click(bigCookie_button).perform()    

    # To get the final ratio
    # cookies = driver.find_element(By.XPATH, '//*[@id="cookies"]').text.split()[0].strip() # to track cookies after upgrade            
    # print(" Cookies per second: ",cookies,"\n\n\n") 
    
    if time.time()-start_time > 2400:    
        break

########################### CLOSING BROWSER ###########################
#driver.close() # current windows
driver.quit() # entire browser





