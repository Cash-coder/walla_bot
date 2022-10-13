from json.encoder import ESCAPE
from walla_bot3 import importDataFrom, set_driver, load_cookies, \
    save_cookies, BackupLastUsedCookies, close_second_tab, my_click, \
    type_text, setFirefoxDriver
from multiprocessing import Process, cpu_count
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
import traceback
import time


#this programe runs over all prods in a walla account to perform 3 possible actions in this order
#remove the ad if the prod is no longer present in prodsDB
#upate the price if it has changed
#if none of the above were executed (prod present with the same price):
#   reupload the ad to gain more traffic

#open walla, in products page use the prodTitle 
#to query the prodsDB
#find the best price for that product (in case it had changed) and update adPrice
#if Title does't exist, remove it from walla
# import py file with proxy data from another folder


PASS_FILE_PATH = r'C:\Users\HP EliteBook\OneDrive\A_Miscalaneus\Escritorio\Code\git_folder\sm_sys_folder\pass_module.py'

def generateDescription(minPrice):
    #example: '3 pagos de 150€ = 450€'
    oneInstallmentPrice = int(minPrice/3)
    installmentText = f"3 pagos de {oneInstallmentPrice}€ = {minPrice}"

    #version with installment payment
    updatedDescription = f"""✨ Smart-Market ✨ 
Todos nuestros productos cuentan con garantía de hasta 3 años ⭐️
Precio aplazado en 3 cómodos pagos: {installmentText} ⭐️
Producto de Segunda Mano sin abrir ni reparaciones⭐️
Puedes ver fotos reales de cada producto en nuestra web ⭐️
Entregamos factura de compra y garantía ⭐️
Ofrecemos muchos más precios y modelos en nuestra web ⭐️
Envío Gratis a domicilio 24h ⭐️
Compras en nuestra web ⭐️
Te damos tiempo para que lo veas y pruebes en persona⭐️
Te desamos feliz compra ⭐️
✨  Smart-Market ✨
"""
    return updatedDescription
    

def importPassFile():
    import sys
    sys.path.insert(0, PASS_FILE_PATH)
    import pass_module
    return pass_module.DB_PASSWD

def SetDbConnector():
    import mysql.connector
    
    module = importDataFrom('pass_module.py', PASS_FILE_PATH)
    passwd = module.DB_PASSWD

    mydb = mysql.connector.connect(
        host='localhost',
        user='root',
        passwd= passwd,
        database='prodsdb'
        )
    
    myCursor = mydb.cursor()

    return mydb, myCursor

def DeleteProdRowFromDb(wooId):
    mydb, myCursor = SetDbConnector()

    myCursor.execute(f"DELETE FROM prods WHERE wooId='{wooId}'")
    
    warnings = myCursor.fetchwarnings()
    print('---- MySQL Warnings: ', warnings)

    mydb.commit()

def checkProdPresenceInProdsDb(prod_name, myCursor):
    # myCursor = SetDbConnector()  
    
    myCursor.execute(f'SELECT wpPrice FROM prods WHERE LOWER(targetModel) = "{prod_name}"')
    r = myCursor.fetchall()
    
    #if no matches return false
    if r == []:
        # print(f'missing this prod name: {prod_name}')
        return False
    else:
        return True


def removeProdFromWalla(prod, d):
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC

    #mark as selled
    time.sleep(1)
    prod.find_element(By.XPATH, './/button[@class="btn-sold ng-star-inserted"]').send_keys(Keys.ENTER)

    #press in "sold outside of walla"
    wait = WebDriverWait(d, 10)
    target = wait.until(EC.visibility_of_element_located((By.XPATH, '//div[@class="modal-footer"]/a')))
    target.send_keys(Keys.ENTER)
    time.sleep(2)    

def updateWallaProdPrice(d, ad, myCursor, city):
    
    title         = ad.find_element(By.XPATH, './/span[@class="info-title subtitle"]').text.lower()
    current_price = float(ad.find_element(By.XPATH, './/span[@class="info-price"]').text.replace('€', '').replace('.', '').replace(',', '.'))

    myCursor.execute(f'SELECT WpPrice FROM prods WHERE LOWER(targetModel) = "{title}"')
    pricesList = myCursor.fetchall()
    intList = [int(price[0].split('.')[0]) for price in pricesList]

    # if current price is min price, do nothing
    minPrice = min(intList)
    installmentPrice = int(minPrice/3)

    if installmentPrice == current_price:
        #false because the price is the same, 
        #the return will be used to trigger just an update to grain traffic
        return False 

    # Bug Fix:
    # InterceptionError, other element will receive the click
    # sleep or
    # d.switch_to.active_element

    # if current price is different than minPrice in DB:
    print(f'city: {city}, price change in: {title}, currentPrice: {current_price}, minPrice: {minPrice}, installment: {installmentPrice}')
    # click in edit
    ad.find_element(By.XPATH, './/button[@class="btn-edit ng-star-inserted"]').send_keys(Keys.RETURN)
    time.sleep(5)
    
    # sometimes weigth is uncheked
    d.find_elements(By.XPATH , '//label[@class="WeightSelector btn ng-star-inserted"]/input')[0].click()

    # text update (installments price)
    UpdateText(d, minPrice)
    time.sleep(2)
   
    # Price update with RETURN at the end
    updatePrice(d, installmentPrice)
    time.sleep(2)

    # signal the prodPrice has been update
    return True

def UpdateText(d, minPrice):
    
    #generate description updated with new price
    updatedText = generateDescription(minPrice)
    
    # click in textarea
    textArea = d.find_element(By.XPATH ,'//textarea')
    textArea.click()
    time.sleep(0.3)

    # chain remove old text Cn+a, delete
    ActionChains(d).key_down(Keys.CONTROL).send_keys("a")\
        .send_keys(Keys.DELETE).key_up(Keys.CONTROL).perform()
    time.sleep(0.3)

    #paste new text
    textArea.send_keys(updatedText)
    time.sleep(0.5)


def updatePrice(d, minPrice):
    from selenium.common.exceptions import ElementClickInterceptedException
    import traceback
    
    # click in price avoiding bugs
    attempts = 0
    while attempts < 2:
        try :
            time.sleep(2)
            # d.switch_to.active_element

            priceInputXpath = '//input[@id="price"]'
            # priceInputXpath = '//label[@for="price"]'
            priceInput = d.find_element(By.XPATH, priceInputXpath)
            
            action = ActionChains(d)
            action.click(on_element= priceInput).perform()
            # priceInput.click()
            
            break

        except ElementClickInterceptedException:
            print(f'element Interception Exception dected, trying again ...')
            # print(traceback.format_exc)
            attempts += 1

    # remove old price
    ActionChains(d).key_down(Keys.CONTROL).send_keys("a")\
        .send_keys(Keys.DELETE).key_up(Keys.CONTROL).perform()

    # send new price
    d.find_element(By.XPATH, priceInputXpath).send_keys(minPrice)
    time.sleep(1)
    d.find_element(By.XPATH, priceInputXpath).send_keys(Keys.ENTER)

    time.sleep(5)    

def updateProd(ad, d):

    # title = ad.find_element(By.XPATH, './/span[@class="info-title subtitle"]').text.lower()
    
    #enter on update button
    ad.find_element(By.XPATH, './/button[@class="btn-edit ng-star-inserted"]').send_keys(Keys.RETURN)
    time.sleep(6)
    
    #sometimes shipping button is not marked
    #[0]:2kg, [1]:5kg, etc...
    d.find_elements(By.XPATH , '//label[@class="WeightSelector btn ng-star-inserted"]/input')[0].click()

    #return on prod's page update button
    # d.find_element(By.XPATH, '//span[contains(text(), "Actualizar")]').send_keys(Keys.RETURN)
    d.find_element(By.XPATH, '//button[@class="btn btn-block btn-primary"]').send_keys(Keys.RETURN)

    time.sleep(3)

    # return to catalog page
    # sometimes it gets stucked for walla errors
    d.get('https://es.wallapop.com/app/catalog/published')

def closePrivacyBanner(d):

    try:
        banner = d.find_element(By.XPATH, '//button[@id="onetrust-accept-btn-handler"]')
        if banner:
            banner.click()
    except Exception as e:
        print(e)
        pass

# wait until you load all the prods of the page
# this compares len(ads) the 1º time you loaded page with 15'' sleep
# with current len(ads)
def specialSleep(d, totalAds, adsXpath):

    while True:
        currentLen = len(d.find_elements(By.XPATH, adsXpath))
        
        #finish when current loaded ads == totalAds
        if currentLen == totalAds:
            return
        else:
            time.sleep(0.5)


def selectAd(ads, adsTitles, n):
    
    targetTitle = adsTitles[n].strip()

    for ad in ads:
        title = ad.find_element(By.XPATH, './/span[@class="info-title subtitle"]').text.lower().strip()
        if title == targetTitle:

            try:
                return ad, title
            except Exception as e:
                print(e, '\n')
                            
                for ad in ads:
                    title = ad.find_element(By.XPATH, './/span[@class="info-title subtitle"]').text.lower().strip()
                    print(f'p: {title}')
                    if title == targetTitle:
                        return title
    # print(f"Can't find the targetTitle: '{targetTitle}' in the TitlesList: {adsTitles}")

def getAdsTitles(d, adsXpath):

    titles = []

    ads = d.find_elements(By.XPATH, adsXpath)
    for ad in ads:
        title = ad.find_element(By.XPATH, './/span[@class="info-title subtitle"]').text.lower()
        titles.append(title)
    
    return titles 


def run(proxyN, headless):
    
    mydb, myCursor = SetDbConnector()  
    
    d, city = setFirefoxDriver(proxyN, headless)
    close_second_tab(d)

    #accept cookies banner
    #closePrivacyBanner(d)

    d.get('https://es.wallapop.com/app/catalog/published')
    time.sleep(12) #let prods page to load all prods

    #every time you update an ad
    #walla relocates the ad in the serp, breaking indexes
    #the relocation breaks the index order
    #so, use the title to select the ad
    #adsTitles[n]
    adsXpath = '//div[@class="row CatalogItem__content"]'
    ads = d.find_elements(By.XPATH, adsXpath)
    totalAds = len(ads)
    adsTitles = getAdsTitles(d, adsXpath)

    for n in range(totalAds):
        try:
            specialSleep(d, totalAds, adsXpath)

            ads = d.find_elements(By.XPATH, '//div[@class="row CatalogItem__content"]')
            ad, title = selectAd(ads, adsTitles, n)

            #pick some specific prod title
            # if 'iphone 8' not in title:
            #     continue

            #if prod is not present in DB
            if not checkProdPresenceInProdsDb(title, myCursor):
                print(f'{city}: this prod title is not in the database: {title}, removing ...')
                removeProdFromWalla(ad, d)
                continue

            #update prod price, if it has been updated got to the next prod
            if updateWallaProdPrice(d, ad, myCursor, city):
                continue

            #if prod still exists and hasn't changed
            #update to gain traffic
            print(f"{city}: going to just update this prod: {title}")
            adTitle = ad.find_element(By.XPATH, './/span[@class="info-title subtitle"]').text.lower()
            updateProd(ad, d)
            time.sleep(2)

        except Exception as e:
            print(e)
            traceback.print_exc()
            pass
    
    d.close()


def main():
    
    headless = True
    a = Process(target=run, args=(0, headless))
    b = Process(target=run, args=(1, headless))
    c = Process(target=run, args=(2, headless))
    
    a.start()
    time.sleep(1)
    b.start()
    time.sleep(1)
    c.start()
    
    a.join()
    b.join()
    c.join()

    #test one in isolated way, without headless
    # headless = False
    # run(1, headless)

    print(f'finish time in {time.perf_counter()} secs')


if __name__ == "__main__":
    main()