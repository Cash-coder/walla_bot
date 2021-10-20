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

COOKIES_FILE = r'C:\Users\HP EliteBook\OneDrive\A_Miscalaneus\Escritorio\Code\git_folder\chatbot\walla_chat\cookies_new.pkl'
PRODUCTS_FILE = r'C:\Users\HP EliteBook\OneDrive\A_Miscalaneus\Escritorio\Code\git_folder\walla_bot\prods.json'

def login_cookies(d, COOKIES_FILE):
    ''' d, COOKIES_FILE '''
    import pickle
    try:
        logging.info(f'using COOKIES_FILE: {COOKIES_FILE}')
        d.get('https://es.wallapop.com/')
        cookies = pickle.load(open(COOKIES_FILE, "rb"))
        for cookie in cookies:
            if cookie['domain'] == '.wallapop.com':
                logging.info(f'added this cookie: {cookie}')
                d.add_cookie(cookie)
        sleep(1)
        d.get('https://es.wallapop.com/app/catalog/upload')
        logging.info('successful login')
        sleep(2)

        save_cookies(d, COOKIES_FILE='cookies_new.pkl')
        print('logged in successfully')
        return 'success'
    except Exception as e:
        print(f'error in login_cookies(): {e}')
        return 'login error'

def save_cookies(d, COOKIES_FILE='unspecified'):
    ''' d, COOKIES_FILE // if COOKIES_FILE name not specified = cookies_last_login.pkl '''
    import pickle

    if COOKIES_FILE == 'unspecified':
        COOKIES_FILE = "cookies_last_login.pkl" 
    
    with open(COOKIES_FILE, "wb") as f:
        pickle.dump( d.get_cookies(), f)
    logging.info(f'login cookies saved in file {COOKIES_FILE}')

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

def login_form(d, email, password):
    pass

def my_click(d, xpath): 
    print('going to click:', xpath)
    wait = WebDriverWait(d, 5)
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
        
        # sleep(3)
    except Exception as e:
        print(e)

def type_text(d, text, xpath, end='unspecified'):
    ''' d, xpath, text, end: tab, enter'''
    element = d.find_element(By.XPATH, xpath)
    element.send_keys(text)
    
    if end == 'tab':
        element.send_keys(Keys.TAB)
    elif end == 'enter':
        element.send_keys(Keys.ENTER)



def select_prod_state(d, prod_state):
    ''' d , prod_state'''
    print(f'in select_prod_state() prod_state: {prod_state}')
    try:#open dropdown list
        my_click(d, '//div[contains(text(), "Escoge un estado")]')
        #select based on prod_state
        if prod_state == 'new':
            my_click(d, '//li[contains(text(), "Nuevo")]')
        elif prod_state == 'like new':
            my_click(d, '//li[contains(text(), "Como nuevo")]')
        elif prod_state == 'good state':
            my_click(d, '//li[contains(text(), "En buen estado")]')
        elif prod_state == 'acceptable state':
            my_click(d, '//li[contains(text(), "En condiciones aceptables")]')
        elif prod_state == 'd state':
            my_click(d, '//li[contains(text(), "Lo ha dado todo")]')
    except Exception as e:
        print(f'error in select_prod_state() : {e}')
        traceback.print_exc()

def insert_pics(d, pics):
    print(f' in insert_pics()  pics: {pics}')
    # r'C:\Users\HP EliteBook\OneDrive\A_Miscalaneus\Imágenes\4Oscuro.jpg'
    # ["C:\\Users\\HP EliteBook\\OneDrive\\A_Miscalaneus\\Imágenes\\4Oscuro.jpg", "C:\\Users\\HP EliteBook\\OneDrive\\A_Miscalaneus\\Imágenes\\2oscuro.jpg","C:\\Users\\HP EliteBook\\OneDrive\\A_Miscalaneus\\Imágenes\\3oscuro.jpg"]
    #pics = [r'C:\Users\HP EliteBook\OneDrive\A_Miscalaneus\Imágenes\4Oscuro.jpg', r'C:\Users\HP EliteBook\OneDrive\A_Miscalaneus\Imágenes\2oscuro.jpg', r'C:\Users\HP EliteBook\OneDrive\A_Miscalaneus\Escritorio\iphone-13_2.jpg', r'C:\Users\HP EliteBook\OneDrive\A_Miscalaneus\Escritorio\iphone13_1.jpg']
    # pic = 'https://mega.co.nz/#!SrBgjByT!xXMd75g13YVk_iAgdcOhAJ5FDZRU4NWDqlyYGGTska8'
    
    pics_input_xpath = '//input[@type="file"]'
    pic_inputs = d.find_elements(By.XPATH, pics_input_xpath)
    
    #wallapop has 10 different pic input paths, one for each pic, so zip each pic with a unique input
    zipped_list = zip(pics, pic_inputs)
    
    for entry in zipped_list:
        try:
            pic = entry[0]
            input = entry[1]

            input.send_keys(pic)
            print(f'pic: {pic}')
            print(f'input: {input}')

            print('inserted pic')
        except Exception as e :
            print(' error in insert_pics(): ', e)
            traceback.print_exc()

def upload_ad(  d,
                prod_title,
                prod_state,
                prod_description,
                price,
                prod_brand,
                prod_model,
                location,
                pics,
                category,
                subcategory = 'not needed'
                ):

    global total_published_ads

    try:
        # if driver not in upload ad page, click in upload new ad
        if d.current_url != 'https://es.wallapop.com/app/catalog/upload' :
            my_click(d, '//span[contains(text(), "Subir producto")]')
        
        #click in "algo que ya no necesito"
        my_click(d, '//span[contains(text(), "Algo que ya no necesito")]')
        #prod title
        type_text(d, prod_title ,'//input[@placeholder="En pocas palabras..."]')
        #price
        type_text(d, price ,'//input[@placeholder="(No te pases)"]')
        # category
        select_category(d, category, subcategory)        
        #prod state (sin abrir, nuevo, como nuevo, en buen estado, en condiciones aceptables, lo ha dado todo)
        select_prod_state(d, prod_state)
        #fill prod_description
        type_text(d, prod_description, '//textarea')
        #fill brand (iphone)
        brand_input_xpath = '//input[@placeholder="P. ej: Apple"]'
        type_text(d, prod_brand, brand_input_xpath, end='tab')
        #type TAB to drop up brands list
        brand_input = d.find_element(By.XPATH, brand_input_xpath)
        brand_input.send_keys(Keys.TAB)
        #fill model (iphone 12)
        type_text(d, prod_model, '//input[@placeholder="P. ej: iPhone"]', end='tab')
        #upload pics, list of absolute paths
        insert_pics(d, pics)     
        #click in shipping 2Kg
        my_click(d, '//span[contains(text(), "2kg")]')
        #type location
        type_text(d, location, '//input[@placeholder="Marca la localización"]')
        my_click(d, '//button[contains(text(), "Aplicar")]')

        sleep(4)

        #click in submit
        my_click(d, '//button[@class="btn btn-block btn-primary"]')
        #click in close "Genial tu producto ya está subido, queres destacarlo ?"
        my_click(d , '//div[@class="modal-close light"]')
        
        # '//tsl-svg-icon[@src="/assets/icons/cross.svg"]'

        try:
            success_text = d.find_element(By.XPATH, '//h1[contains(text(), "¡Genial! Tu producto ya está en Wallapop")]').text
            # success_text_xpath = '//h1[contains(text(), "¡Genial! Tu producto ya está en Wallapop")]'
            
            # wait = WebDriverWait(d, 10)
            # success_text = wait.until(
            # EC.presence_of_element_located((By.XPATH, success_text_xpath)))

            if success_text != None:
                return 'success'
        except Exception as e:
            print(e)
            traceback.print_exc()
            print(f'not uploaded this ad {prod_title}')

    except Exception as e:
        print(f'---error in upload_ad(), error: {e}')
        traceback.print_exc()
        return 'uploading error'
    
    # if total_published_ads == prod_len-1: # -1 because the 1º is credentials
    #     print('published all ads, driver closed')           
    #     d.close()

def select_category(d, category, subcategory='not needed'):
    print(f'category inside select_category(): {category}')
    if category == 'smartphones':
        my_click(d, '//tsl-dropdown[@placeholder="Categoría"]')
        my_click(d, '//div[contains(text(), " Móviles y Telefonía ")]') #notice it has spaces at both sides
        my_click(d, '//tsl-dropdown[@placeholder="Subcategoría"]')
        my_click(d, '//span[contains(text(), "Teléfonos móviles")]')


def run():
    global total_published_ads
    d = set_driver()
    with open('prods.json', encoding='utf8') as f:
        json_data = json.load(f)
        # print(f'json data sample: {json_data[1:3]}')

    #get credentials
    credentials =  json_data[0]
    logging.info(f'credentials {credentials}')

    COOKIES_FILE = credentials.get('login_cookies_file')
    walla_user =  credentials.get('walla_user')
    walla_password =  credentials.get('walla_password')

    prods_len = len(json_data) #len of all prods, to know when to close the driver
    print(f'this is json len {prods_len}')

    # print('this are the credentials',
                # COOKIES_FILE,'\n',
                # walla_user, 
                # walla_password)

    result = login_cookies(d, COOKIES_FILE)
    if result == 'login error':
        try:
            print('loging error! trying login form')
            login_form(d) #login manually filling email and password and bypassing captcha.
        except:
            print('Could not login, program closed')
            return

    total_published_ads = 0
    for prod in json_data[1:]: #avoid the 1º where the credentials are
        try:
            #read json with products to upload
            #for prod in products:
            prod_title = prod.get('wallapop_title')
            prod_state = prod.get('prod_state')
            prod_description = prod.get('ad_text')
            price = prod.get('selling_price')
            prod_brand = prod.get('prod_brand')
            prod_model = prod.get('prod_model')
            location = prod.get('location')
            pics = prod.get('pics')
            category = prod.get('category')

            print(f'prod_title {prod_title} \n, prod_state {prod_state} \n, prod_description {prod_description} \n, price {price} \n, prod_brand {prod_brand} \n, prod_model {prod_model} \n, location {location} \n, pics {pics} \n, category')

            result = upload_ad(d,prod_title = prod_title,
                                prod_state = prod_state,
                                prod_description = prod_description,
                                price = price,
                                prod_brand = prod_brand,
                                location = location,
                                pics = pics,
                                prod_model = prod_model,
                                category = category
                                )
            
            #errors are handled inside upload_ad()
            if result == 'uploading error':
                continue
            elif result == 'success':
                total_published_ads += 1
                print(f'total published ads: {total_published_ads} of {prods_len} total // new ad published: {prod_title}')


        except Exception as e:
            print(f'error in loop uploading prods prod_title: {prod_title}, error message: \n {e}')
            continue
    
    print(f'published all ads: {total_published_ads}, driver closed')           
    d.close()

    

if __name__ == "__main__":
    run()