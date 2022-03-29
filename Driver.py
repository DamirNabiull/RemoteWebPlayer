from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import json
import logging


logging.basicConfig(filename='app_player.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')


class MyDriver:
    __instance = None

    def __init__(self):
        if not MyDriver.__instance:
            file = open('config.json')
            self.data = json.load(file)

            chrome_options = Options()
            chrome_service = Service(self.data[self.data['platform']])
            chrome_options.add_experimental_option("useAutomationExtension", False)
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_argument("--kiosk")

            self.driver = webdriver.Chrome(service=chrome_service,
                                      options=chrome_options)

            self.driver.set_page_load_timeout(5)
            if self.data['show'] == 'url':
                try:
                    self.driver.get(self.GetLink())
                except Exception as e:
                    page_state = self.driver.execute_script('return document.readyState;') == 'complete'
                    logging.warning(f'Start : {page_state}')
            else:
                try:
                    path = self.data['projectPath']
                    self.driver.get(rf'{path}\image.png')
                except Exception as e:
                    page_state = self.driver.execute_script('return document.readyState;') == 'complete'
                    logging.warning(f'Start : {page_state}')


    @classmethod
    def getInstance(cls):
        if not cls.__instance:
            cls.__instance = MyDriver()
        return cls.__instance

    def GetDriver(self):
        return self.driver

    def GetLink(self):
        return self.data['url']
