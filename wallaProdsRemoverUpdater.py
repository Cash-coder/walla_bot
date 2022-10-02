from json.encoder import ESCAPE
from walla_bot3 import importDataFrom, set_driver, load_cookies, \
    save_cookies, BackupLastUsedCookies, close_second_tab, my_click, \
    type_text
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
import traceback
from time import sleep


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
    
    myCursor.execute(f'SELECT wpPrice FROM prods WHERE LOWER(wpTitle) = "{prod_name}"')
    r = myCursor.fetchall()
    
    #when there aren't matches mysql returns an empty list
    if r == []:
        print(f'missing this prod name: {prod_name}')
        return False
    else:
        return True


def removeProdFromWalla(prod):
    
    sleep(1)
    prod.find_element(By.XPATH, '//button[@class="btn-sold ng-star-inserted"]').send_keys(Keys.ENTER)
    sleep(3)
    prod.find_element(By.XPATH, '//div[@class="modal-footer"]').click()
    sleep(1)    

def updateWallaProdPrice(d, prod, myCursor):
    
    title         = prod.find_element(By.XPATH, './/span[@class="info-title subtitle"]').text.lower()
    current_price = prod.find_element(By.XPATH, './/span[@class="info-price"]').text.replace('€', '')

    myCursor.execute(f'SELECT WpPrice FROM prods WHERE LOWER(wpTitle) = "{title}"')
    pricesList = myCursor.fetchall()
    floatList = [float(price[0]) for price in pricesList]

    #if current price is min price, do nothing
    minPrice = min(floatList)
    if minPrice >= current_price:
        #false because the price is ok, 
        #the return will be used to trigger just an update to grain traffic
        return False 

    #if current price is higher than minPrice in DB:
    print(f'there is a lower price for this prod: {title}, currentPrice: {current_price}, minPrice: {minPrice}')
    prod.find_element(By.XPATH, '//button[@class="btn-edit ng-star-inserted"]').send_keys(Keys.RETURN)
    sleep(5)
    
    #click in price
    priceInput = d.find_element(By.XPATH, '//input[@id="price"]')
    priceInput.click()

    # remove old price
    ActionChains(d).key_down(Keys.CONTROL).send_keys("a")\
        .send_keys(Keys.DELETE).key_up(Keys.CONTROL).perform()

    #send new price
    priceInput.send_keys(minPrice)
    priceInput.send_keys(Keys.ENTER)

    #signal the prodPrice has been update
    return True

def updateProd(prod):
    
    #enter on update button
    prod.find_element(By.XPATH, '//button[@class="btn-edit ng-star-inserted"]').send_keys(Keys.RETURN)
    sleep(4)

    #return on prod's page update
    prod.find_element(By.XPATH, "//span[contains(text(), 'Actualizar')").send_keys(Keys.RETURN)



def run():
    
    mydb, myCursor = SetDbConnector()  
    
    for i in range(3):
        d, city = set_driver(i)
        close_second_tab(d)
        d = load_cookies(d, city)
    
        #accept cookies banner
        my_click(d, '//button[@id="onetrust-accept-btn-handler"]')
        d.get('https://es.wallapop.com/app/catalog/published')
        sleep(8) # let prods page to load all prods

        ads = d.find_elements(By.XPATH, '//div[@class="row CatalogItem__content"]')
        for ad in ads:
            title = ad.find_element(By.XPATH, './/span[@class="info-title subtitle"]').text.lower()
            
            #if prod is not present in DB
            if not checkProdPresenceInProdsDb(title, myCursor):
                print(f'this prod title is not in the database: {title}')
                removeProdFromWalla(ad)
                continue

            #update prod price, if it has been updated got to the next prod
            if updateWallaProdPrice(d, ad, myCursor):
                continue

            #if prod still exists and hasn't changed
            #update to gain traffic
            updateProd(ad)

        #save cookies after going over all prods        
        save_cookies(d, city)


if __name__ == "__main__":
    run()