from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time, traceback, threading,sys
import os
from threading import Thread
import keyboard


class press_detect(Thread):
    

    key = False
    key_combo = keyboard.get_hotkey_name(['ctrl','alt','n'])
    status = True
    skip_val = False
    def __init__(self):
        Thread.__init__(self)
    def run(self):
        keyboard.add_hotkey(self.key_combo, self.val)
        while self.status is True:
            if(self.key is True):
                self.skip_val = True
                self.key = False
    def val(self):
        self.key = True
    def skip(self):
        if(self.skip_val is True):
            self.skip_val = False
            return True
        else:
            return False
pd = press_detect()
pd.start()


chrome_options = Options()
#chrome_options.add_argument("--disable-extensions")
#chrome_options.add_argument("--headless")
#chrome_options.add_argument("--test-type")
#chrome_options.add_argument('--ignore-certificate-errors')
#chrome_options.add_argument('--ignore-urlfetcher-cert-requests')
driver = webdriver.Chrome(chrome_options=chrome_options)

driver.get("http://music.youtube.com")

while not pd.skip():
    time.sleep(1)

start = False
while not start:
    try:
        start_music = driver.find_element_by_xpath('//*[@id="items"]/ytmusic-two-row-item-renderer[1]/a/ytmusic-item-thumbnail-overlay-renderer')
        start_music.click()
        start = True
    except:
        time.sleep(1)
        print("sleeping")
print("running skipping")
while True:
    if(pd.skip() is True):
        skipped = False
        while not skipped:
            try:
                start_music = driver.find_element_by_xpath('//*[@id="left-controls"]/div/paper-icon-button[3]')
                start_music.click()
                skipped = True
            except:
                time.sleep(0.01)
                

#driver.exit()


