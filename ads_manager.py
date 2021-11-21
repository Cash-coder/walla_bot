# reads ads_db
# in ads_db is marked which products are uploaded and which not.
#takes not uploaded prods
#creates a json for each wallapop / milanuncios account
    #that json is the same, but with changed loggin data and prod location
#ads_uploader reads json and uploads

#at the start of the program, it takes log file if any, and updates ads_db

import csv
from re import S, sub
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options

from time import sleep
import json
import undetected_chromedriver.v2 as uc

