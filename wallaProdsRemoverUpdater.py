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

#site with prods
# https://es.wallapop.com/app/user/ericr-404394075-nz0mmk5ggvjo/published
# great phones: https://es.wallapop.com/app/user/taraa-79069256-lqzmpq7dgozv/published
#g drive spreadshit + phone (teneis teléfono? tengo un marketplace de prods en el que podrías vender)

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

    #if current price is min price, do nothing
    minPrice = min(intList)
    if minPrice == current_price:
        #false because the price is the same, 
        #the return will be used to trigger just an update to grain traffic
        return False 

    #if current price is different than minPrice in DB:
    print(f'city: {city}, there is a lower price for this prod: {title}, currentPrice: {current_price}, minPrice: {minPrice}')
    #click in edit
    ad.find_element(By.XPATH, './/button[@class="btn-edit ng-star-inserted"]').send_keys(Keys.RETURN)
    time.sleep(5)
    
    #click in price
    priceInput = d.find_element(By.XPATH, '//input[@id="price"]')
    priceInput.click()

    #remove old price
    ActionChains(d).key_down(Keys.CONTROL).send_keys("a")\
        .send_keys(Keys.DELETE).key_up(Keys.CONTROL).perform()

    #send new price
    priceInput.send_keys(minPrice)
    priceInput.send_keys(Keys.ENTER)

    time.sleep(8)    

    #signal the prodPrice has been update
    return True

def updateProd(ad, d):

    title = ad.find_element(By.XPATH, './/span[@class="info-title subtitle"]').text.lower()
    
    #enter on update button
    ad.find_element(By.XPATH, './/button[@class="btn-edit ng-star-inserted"]').send_keys(Keys.RETURN)
    time.sleep(6)

    #return on prod's page update
    # d.find_element(By.XPATH, '//span[contains(text(), "Actualizar")]').send_keys(Keys.RETURN)
    d.find_element(By.XPATH, '//button[@class="btn btn-block btn-primary"]').send_keys(Keys.RETURN)

    time.sleep(6)

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


def run(proxyN):
    
    mydb, myCursor = SetDbConnector()  
    
    d, city = setFirefoxDriver(proxyN)
    close_second_tab(d)

    #accept cookies banner
    #closePrivacyBanner(d)

    d.get('https://es.wallapop.com/app/catalog/published')
    time.sleep(12) #let prods page to load all prods

    adsXpath = '//div[@class="row CatalogItem__content"]'
    ads = d.find_elements(By.XPATH, adsXpath)
    totalAds = len(ads)
    adsTitles = getAdsTitles(d, adsXpath)

    for n in range(totalAds):
        try:
            specialSleep(d, totalAds, adsXpath)

            #every time you update an ad
            #walla relocates the ad in the serp, breaking indexes
            #the relocation breaks the index order
            #so use the title to select the ad
            #adsTitles[n]
            ads = d.find_elements(By.XPATH, '//div[@class="row CatalogItem__content"]')
            ad, title = selectAd(ads, adsTitles, n)
            
            #if prod is not present in DB
            if not checkProdPresenceInProdsDb(title, myCursor):
                print(f'{city}: this prod title is not in the database: {title}, removing ...')
                removeProdFromWalla(ad, d)
                continue

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
    #save cookies after going over all prods        
    # save_cookies(d, city)


def main():
    
    a = Process(target=run, args=(0,))
    b = Process(target=run, args=(1,))
    c = Process(target=run, args=(2,))
    
    a.start()
    time.sleep(1)
    b.start()
    time.sleep(1)
    c.start()
    
    a.join()
    b.join()
    c.join()

    #test one in isolated way, without headless
    # run(2)

    print(f'finish time in {time.perf_counter()} secs')


if __name__ == "__main__":
    main()