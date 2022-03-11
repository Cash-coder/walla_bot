# -*- coding: utf-8 -*-
#wallapop es como Amazon, se vende de todo: https://es.wallapop.com/app/user/oferta-365057118-x6qkp0vwgq6y/reviews
#busca algunos de sus productos con b´suqueda por imágen ?
import json
import traceback
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

COOKIES_FOLDER = r'C:\Users\HP EliteBook\OneDrive\A_Miscalaneus\Escritorio\Code\git_folder\mila_bot\cookies_folder\\'
from selenium.common.exceptions import TimeoutException


# def set_driver():
#     print('setting driver...')
#     options = uc.ChromeOptions()
#     # options.add_argument('--no-sandbox')
#     # options.add_argument('--headless')
#     # options.add_argument('--disable-gpu')
#     # options.add_argument("--window-size=1920, 1200")
#     # options.add_argument('--disable-dev-shm-usage')

#     d = uc.Chrome(options=options)
#     d.maximize_window()
    
#     print(f'driver set. Session id: {d.session_id}')
#     return d


def set_driver():
    print('setting driver...')
    from selenium import webdriver

    options = uc.ChromeOptions()
    # options = webdriver.ChromeOptions()
    # options.headless = True
    options.add_argument('--headless')
    options.add_argument("--no-sandbox")
    options.add_argument('--disable-gpu')
    options.add_argument("--window-size=1920,1200")
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("--window-size=1920,1080")
    options.add_argument("start-maximized")
    options.add_argument('--no-first-run --no-service-autorun --password-store=basic')

    d = uc.Chrome(options=options)
    d.set_page_load_timeout(12)


def my_get(d, url):
    print(f'going to get {url}')
    try:
        d.get(url)
        print('url gog')
    except TimeoutException as timeout:
        print('time out exception in get, getting again')
        d.get(url)


def my_click(d, xpath): 
    #print(colored("Executed Click!!XXXXXXXXXXXXXXXXXXXXXXXXXXXXXx",'white','on_green'))        
    print(f'going to click {xpath}')
    try:
        wait = WebDriverWait( d, 10) #d = driver
        target = wait.until(
        EC.element_to_be_clickable((By.XPATH, xpath)))

        # print('going to click:',xpath)
        #target.click()
        #Action chains has little accuracy, lots of mistakes clicking in the wrong plage
        actions = ActionChains(d)
        actions.move_to_element(target).click().perform()
        # print('clicked')

        try:
            d.switch_to.active_element
        except Exception as e:
            print(e)
        # sleep(4)
        print('clicked!')
    except Exception as e:
        print(e)
        traceback.print_exc()
        pass


def login_cookies(d, account_mail, url):
    from selenium.common.exceptions import TimeoutException
    import pickle

    cookies_file = get_cookies_filepath(account_mail)
    if cookies_file == 'file not found':
        return 'login error'
    try:
        cookies_filepath = COOKIES_FOLDER  + cookies_file
        # cookies_filepath = r'C:\Users\HP EliteBook\OneDrive\A_Miscalaneus\Escritorio\Code\git_folder\chatbot\walla_chat\cookies_new.pkl'
        # print(f'using cookies_filepath: {cookies_filepath}')
        # d.get(url)
        my_get(d, url)
        cookies = pickle.load(open(cookies_filepath, "rb"))
        for cookie in cookies:
            if 'sameSite' in cookie: #used to avoid google error with cookies
                if cookie['sameSite'] == 'None':
                    cookie['sameSite'] = 'Strict'
            d.add_cookie(cookie)
            # print(f'added this cookie: {cookie}')

        my_get(d, url)
        sleep(3)

        #check if login was successful, save cookies
        user_avatar = '//span[@class="ma-UserAvatar"]'
        r = check_presence(d, user_avatar)
        if r == 'present':
            print('logged in successfully, saving cookies...')
            save_cookies(d, COOKIES_FILE_PATH=cookies_filepath)
            print(f'cookies saved {cookies_file}')
            return 'success'
        elif r == 'not present':
            return 'login error'

    except TimeoutException: #sometimes takes too long to load the page, if reaload the url it work
        print('selenium TimeOut exceptiopn, going to reaload the page')
        d.get(url)
        sleep(5)
        
    except Exception as e:
        print(f'error in login_cookies(): {e}')
        traceback.print_exc()
        return 'login error'

def check_presence(d, xpath):
    print(f'checking if xpath is prenset: {xpath}')
    try:
        # login_button_xpath = '//button[@class="BtnLogin"]'
        login_button = d.find_element(By.XPATH, xpath)

        print(f'this element it\'s present {login_button.text}')

        if login_button != None:
            print('xpath is present')
            return 'present'
    except:
        print(f'xpath, is NOT prenset: {xpath}')
        return 'not present'

def get_cookies_filepath(account_mail):
    import os
    global COOKIES_FOLDER
    
    all_cookie_files = os.listdir(COOKIES_FOLDER)
    for file_path in all_cookie_files:
        if account_mail in file_path:
            return file_path
    return 'file not found'

def save_cookies(d, COOKIES_FILE_PATH):
    import pickle
    #sometimes I use the account mail to save cookies
    if '\\' not in COOKIES_FILE_PATH:
        COOKIES_FILE_PATH = COOKIES_FOLDER + COOKIES_FILE_PATH + '.pkl'

    with open(COOKIES_FILE_PATH, "wb") as f:
        pickle.dump( d.get_cookies(), f)

d = set_driver()
account_mail = 'smartmarketalmeria@gmail.com'
login_cookies(d,account_mail, 'https://www.milanuncios.com/')

my_click(d, '//div[@class="ma-CategoriesCategoryHighlightedCard-info"]')
my_click(d, '//div[@class="ma-CategoriesCategoryHighlightedCard-info"]')
my_click(d, '//a[@href="/xbox/"]')
my_click(d, '//a[@href="/nintendo-64/"]')