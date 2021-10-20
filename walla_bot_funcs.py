# -*- coding: utf-8 -*-
import undetected_chromedriver.v2 as uc
from selenium.webdriver.common.by import By
import selenium
import time
import random
from time import sleep
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import logging

COOKIES_FILE = r'C:\Users\HP EliteBook\OneDrive\A_Miscalaneus\Escritorio\Code\git_folder\chatbot\walla_chat\cookies_new.pkl'

def cls(): #clears the idle screen
    import os
    os.system('CLS')

def set_driver():
    print('setting driver...')
    
    options = uc.ChromeOptions()
    # options.add_argument('--no-sandbox')
    # options.add_argument('--headless')
    # options.add_argument('--disable-gpu')
    # options.add_argument("--window-size=1920, 1200")
    # options.add_argument('--disable-dev-shm-usage')

    d = uc.Chrome(options=options)
    d.maximize_window()
    
    print('driver set')
    return d

def my_click(d, xpath): 
    print('going to click:',xpath)
    wait = WebDriverWait(d, 5) #d = driver
    target = wait.until(
    EC.presence_of_element_located((By.XPATH, xpath)))
    try:
        #target.click()
        #Action chains has little accuracy, lots of mistakes clicking in the wrong plage
        actions = ActionChains(d)
        actions.move_to_element(target).click().perform()
        print('clicked')

        try:
            d.switch_to.active_element
        except Exception as e:
            #print(e)
            print("can't switch to active element")
        sleep(2)
    except Exception as e:
        print(e)