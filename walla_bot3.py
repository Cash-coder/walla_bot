from time import sleep

#load ads to upload
#login in walla using cookies and G user browser
#[upload(ad) for ad in ads]

ADS_FILE = r'C:\Users\HP EliteBook\OneDrive\A_Miscalaneus\Escritorio\Code\git_folder\walla_bot\walla_ads_file.xlsx'

#walla_ads_file.xlsx
#Reference = 1
TITLE_COL=   2
AD_TEXT_COL= 3
PRICE_COL=   4
PICS_COL=    5
CATEGORY=    6
SUBCATEGORY_1_COL=   7
SUBCATEGORY_2_COL=   8
WEIGHT_COL=     9
PROD_STATE_COL= 10
BRAND_COL=      11
MODEL_COL=      12


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

    return d

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
            'cate':    row[CATEGORY],
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

        try:
            d.switch_to.active_element
        except Exception as e:
            #print(e)
            print("can't switch to active element")
        
    except Exception as e:
        print(e)

def type_text(d, text, xpath, end_with='unspecified'):
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.keys import Keys

    element = d.find_element(By.XPATH, xpath)
    element.send_keys(text)
    
    if end_with == 'tab':
        element.send_with_keys(Keys.TAB)
    elif end_with == 'enter':
        element.send_keys(Keys.RETURN)

def upload_ad(ad_data, d):

    # unpack ad_data
    title=    ad_data.get('title')
    ad_text=  ad_data.get('ad_text')
    price=  ad_data.get('price')
    pics=   ad_data.get('pics')
    cate=   ad_data.get('cate')
    weight= ad_data.get('weight')
    brand=  ad_data.get('brand')
    model=  ad_data.get('model')
    subcategory_1=  ad_data.get('subcategory_1')
    subcategory_2=  ad_data.get('subcategory_2')
    prod_state= ad_data.get('prod_state')

    #get the upload new ad url
    if d.current_url != 'https://es.wallapop.com/app/catalog/upload' :
        my_click(d, '//span[contains(text(), "Subir producto")]')
        sleep(3)

    my_click(d, '//span[contains(text(), "Algo que ya no necesito")]')
    sleep(3)



def run():
        
    ads_to_upload = load_prods(ADS_FILE)
    d = set_driver()

    d.get('https://es.wallapop.com/')

    for ad in ads_to_upload:
        try:
            upload_ad(ad, d)
        except Exception as e:
            print(e)


if __name__ == "__main__":
    run()
