from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import json

file = open('config.json')
data = json.load(file)

chrome_options = Options()
chrome_service = Service(data[data['platform']])
chrome_options.add_experimental_option("useAutomationExtension", False)
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_argument("--kiosk");

driver = webdriver.Chrome(service=chrome_service,
                          options=chrome_options)
driver.get(data['url'])
