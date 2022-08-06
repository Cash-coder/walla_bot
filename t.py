#gecko driver firefox allows to send emojies while chromedriver doesn't
def set_gecko_driver():
    from selenium import webdriver
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support import expected_conditions as EC
    

    exe_path     = r'C:\Users\HP EliteBook\OneDrive\A_Miscalaneus\Escritorio\Code\geckodriver.exe'
    profile_path = r'C:\Users\HP EliteBook\AppData\Local\Mozilla\Firefox\Profiles\ct6fc99l.default-release'

    driver = webdriver.Firefox(executable_path=exe_path, firefox_profile=profile_path)
    driver.get('https://www.google.com/')
    
    
    # Chineese Character
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.NAME, "q"))).send_keys("𠀀")
    # Emoji Character
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.NAME, "q"))).send_keys("💩")



def set_gecko_driver_2():
    from selenium import webdriver
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.firefox.options import Options
    

    exe_path     = r'C:\Users\HP EliteBook\OneDrive\A_Miscalaneus\Escritorio\Code\geckodriver.exe'
    profile_path = r'C:\Users\HP EliteBook\AppData\Local\Mozilla\Firefox\Profiles\ct6fc99l.default-release'

    options = Options()
    options.set_preference("-profile", profile_path)

    driver = webdriver.Firefox(executable_path=exe_path)
    driver.get('https://www.google.com/')
    
    
    # Chineese Character
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.NAME, "q"))).send_keys("𠀀")
    # Emoji Character
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.NAME, "q"))).send_keys("💩")


set_gecko_driver_2()

'https://stackoverflow.com/questions/69571950/deprecationwarning-firefox-profile-has-been-deprecated-please-pass-in-an-optio'