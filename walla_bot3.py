from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import traceback
from time import sleep

#load ads to upload
#login in walla using cookies and G user browser
#[upload(ad) for ad in ads]

ADS_FILE    = r'C:\Users\HP EliteBook\OneDrive\A_Miscalaneus\Escritorio\Code\git_folder\walla_bot\walla_ads_file.xlsx'
PICS_FOLDER = r'C:\Users\HP EliteBook\OneDrive\A_Miscalaneus\Escritorio\Code\git_folder\ads_generator\banner_maker\results\results banner girl\\'

#walla_ads_file.xlsx
#Reference = 1
TITLE_COL=   1
AD_TEXT_COL= 2
PRICE_COL=   3
PICS_COL=    4
CATEGORY=    5
SUBCATEGORY_1_COL=   6
SUBCATEGORY_2_COL=   7
WEIGHT_COL=     8
PROD_STATE_COL= 9
BRAND_COL=      10
MODEL_COL=      11


def set_driver():

    import undetected_chromedriver.v2 as uc

    EXECUTABLE_PATH = r'C:\Users\HP EliteBook\OneDrive\A_Miscalaneus\Escritorio\Code\git_folder\login and launcher\chromedriver_old.exe'

    # proxy settings
    # import proxy_data
    # IP_ENTRY  = proxy_data.IP_DICT[proxy_n]
    # IP        = IP_ENTRY.get('ip')
    # CITY      = IP_ENTRY.get('city')
    # HTTPS_PORT = proxy_data.HTTPS_PORT
    # options.add_argument(f'--proxy-server=http://{IP}:{HTTPS_PORT}')

    options = uc.ChromeOptions()
    # this loads the user profile that is logged in wallapop
    options.add_argument(r'--user-data-dir=C:\Users\HP EliteBook\AppData\Local\Google\Chrome\User Data\profile 3')
    options.add_argument('--no-first-run --no-service-autorun --password-store=basic')
    d = uc.Chrome(executable_path=EXECUTABLE_PATH, options=options)
    d.maximize_window()

    #get the upload ad url
    d.get('https://es.wallapop.com/app/catalog/upload')

    return d

#gecko driver firefox allows to send emojies while chromedriver doesn't
def set_gecko_driver():
    from selenium import webdriver
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support import expected_conditions as EC

    driver = webdriver.Firefox(executable_path=r'C:\Utility\BrowserDrivers\geckodriver.exe')
    driver.get('https://www.google.com/')
    # Chineese Character
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.NAME, "q"))).send_keys("𠀀")
    # Emoji Character
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.NAME, "q"))).send_keys("💩")


def load_prods(prods_file):
    from openpyxl import load_workbook
   
    wb = load_workbook(filename = prods_file)
    ws = wb.active
    prod_ads = []

    for row in ws.iter_rows(values_only=True, min_row=2):
        prod_data = {
            'title':   row[TITLE_COL],
            'ad_text': row[AD_TEXT_COL],
            'price':   row[PRICE_COL],
            'pics':    row[PICS_COL],
            'category':    row[CATEGORY],
            'weight':  row[WEIGHT_COL],
            'brand':   row[BRAND_COL],
            'model':   row[MODEL_COL],
            'subcategory_1':  row[SUBCATEGORY_1_COL],
            'subcategory_2':  row[SUBCATEGORY_2_COL],
            'prod_state':     row[PROD_STATE_COL],
                }
        prod_ads.append(prod_data)
    return prod_ads

def my_click(d, xpath): 
    from selenium.webdriver.common.action_chains import ActionChains
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.support.ui import WebDriverWait

    wait = WebDriverWait(d, 5)
    target = wait.until(
        EC.presence_of_element_located((By.XPATH, xpath)))
    try:
        
        #target.click()
        #Action chains has little accuracy, lots of mistakes clicking in the wrong plage
        actions = ActionChains(d)
        actions.move_to_element(target).click().perform()
        # print('clicked')

        sleep(2)

        try:
            d.switch_to.active_element
        except Exception as e:
            #print(e)
            print("can't switch to active element")
        
    except Exception as e:
        print(e)

def type_text(d, text, xpath, sleep_time, end_with='unspecified'):
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver import ActionChains
    import pyperclip

    element = d.find_element(By.XPATH, xpath)
    element.send_keys(text)

    sleep(sleep_time)

    # element.click()
    # d.execute_script("arguments[0].click;", element)
# 
    # pyperclip.copy(text)
    # act = ActionChains(d)
    # act.key_down(Keys.CONTROL).send_keys("v").key_up(Keys.CONTROL).perform()

    
    if end_with == 'tab':
        element.send_with_keys(Keys.TAB)
    elif end_with == 'enter':
        element.send_keys(Keys.RETURN)

# chromedriver doesn't support emojies, so you use pyperclip to copy text to clipboard? and then Control+V in the selected element to paste
def type_text_with_emoji(d, text, xpath, sleep_time):
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver import ActionChains
    import pyperclip

    element = d.find_element(By.XPATH, xpath)
    # element.send_keys(text)
    element.click()
    # d.execute_script("arguments[0].click;", element)

    pyperclip.copy(text)

    act = ActionChains(d)
    act.key_down(Keys.CONTROL).send_keys("v").key_up(Keys.CONTROL).perform()

    sleep(sleep_time)
    

def select_category(d, category, subcategory):
    
    #click in category drop down
    my_click(d, '//tsl-dropdown[@id="category"]')
    sleep(2)

    #in the dropdown menu click element that has text from category parameter
    my_click(d, f'//div[contains(text(), "{category}")]')
    sleep(2)
    
    #click subcategory dropdown menu
    my_click(d, '//tsl-dropdown[@placeholder="Subcategoría"]')

    #click in matching subcategory
    my_click(d, f'//span[contains(text(), "{subcategory}")]')
    sleep(2)

def select_prod_state(d, prod_state):

    #click in prod state dropdown
    my_click(d, '//tsl-dropdown[@id="conditions"]')
    sleep(3)

    # click in dropdown element that matches target prod_state
    my_click(d, f'//li[contains(text(), "{prod_state}")]')
    sleep(2)
    
def insert_pics(d, pic_names, pics_folder):
    
    #locate all 10 pic input paths
    pic_inputs = d.find_elements(By.XPATH, '//input[@type="file"]')

    #wallapop has 10 different pic input paths, one for each pic, so zip each pic with its unique input
    zipped_list = zip(pic_names, pic_inputs)
    
    #insert each pic_local_path into its wallapop_input_path
    for pic_name, input in zipped_list:
        try:

            pic_local_path = pics_folder + pic_name
            print(f'input: {input} \npic: {pic_local_path}')
            input.send_keys(pic_local_path)
        except Exception as e :
                print(' error in insert_pics(): ', e)
                traceback.print_exc()


def upload_ad(d, ad_data):

    # unpack ad_data
    title=    ad_data.get('title')
    ad_text=  ad_data.get('ad_text')
    price=  ad_data.get('price')
    pics=   ad_data.get('pics').split(',')
    weight= ad_data.get('weight')
    brand=  ad_data.get('brand')
    model=  ad_data.get('model')
    category=       ad_data.get('category')
    subcategory_1=  ad_data.get('subcategory_1')
    subcategory_2=  ad_data.get('subcategory_2')
    prod_state= ad_data.get('prod_state')

    # click in upload new ad button
    if d.current_url != 'https://es.wallapop.com/app/catalog/upload' :
        my_click(d, '//span[contains(text(), "Subir producto")]')
        sleep(3)

    #click in "Algo que ya no necesito"
    my_click(d, '//span[contains(text(), "Algo que ya no necesito")]')

    # type prod title
    type_text(d, title ,'//input[@id="headline"]', sleep_time=2)
    
    # price
    type_text(d, price ,'//input[@id="price"]', sleep_time=2)
    
    #type ad text with emoji
    type_text_with_emoji(d, ad_text ,'//textarea[@id="tellUs"]', sleep_time=2)
    
    # type brand | many products don't have brand-model
    if brand:
        type_text(d, brand ,'//input[@placeholder="P. ej: Apple"]', sleep_time=2)
    
    # same for model
    if model:
        type_text(d, model, '//input[@placeholder="P. ej: iPhone"]', sleep_time=2)

    #click in cat and sub_cat
    select_category(d, category, subcategory_1)

    #click and select prod state
    select_prod_state(d, prod_state)

    #insert pics
    insert_pics(d, pics, PICS_FOLDER)

    #click in prod shipping weight | 2, 5, 10, 20, 30 kg
    my_click(d, f'//span[contains(text(), "{weight}")]')

    #LOCATION   
    #upload manually a product with the wanted location, after this Wallapop will remember your selection for future ads

    #click in upload ad
    my_click(d, '//button[@type="submit"]')



def run():
        
    ads_to_upload = load_prods(ADS_FILE)

    d = set_driver()

    upload_ad(d, ads_to_upload[0])
    sleep(1000)

    # for ad in ads_to_upload:

    #     # create a driver on each ad avoids driver disconnect erros
    #     d = set_driver()

    #     try:
    #         upload_ad(d, ad)
    #     except Exception as e:
    #         print(e)
    #     finally:
    #         d.close()
            

if __name__ == "__main__":
    run()
# Consolas y Videojuegos
# Videojuegos