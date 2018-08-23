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
    key_combo_next = keyboard.get_hotkey_name(['ctrl','alt','n'])
    key_combo_pause = keyboard.get_hotkey_name(['ctrl','alt','p'])
    status = True

    key_next = False
    skip_val = False

    key_pause = False
    pause_val = False
    def __init__(self):
        Thread.__init__(self)
    def run(self):
        keyboard.add_hotkey(self.key_combo_next, self.skip_func)
        keyboard.add_hotkey(self.key_combo_pause, self.pause_func)
        while self.status is True:
            if(self.key_next is True):
                self.skip_val = True
                self.key_next = False
            if(self.key_pause is True):
                self.pause_val = True
                self.key_pause = False
    def skip_func(self):
        self.key_next = True
    def pause_func(self):
        self.key_pause = True
    def skip(self):
        if(self.skip_val is True):
            self.skip_val = False
            return True
        else:
            return False
    def pause(self):
        if(self.pause_val is True):
            self.pause_val = False
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

song_name = None
artist = None
album = None
year = None

data_change = [False]*4
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
    if(pd.pause() is True):
        paused = False
        while not paused:
            try:
                start_music = driver.find_element_by_xpath('//*[@id="left-controls"]/div/paper-icon-button[2]')
                start_music.click()
                paused = True
            except:
                time.sleep(0.01)
    try:
        song_element = driver.find_element_by_xpath('//*[@id="layout"]/ytmusic-player-bar/div/div[2]/div[1]/yt-formatted-string')
        song_title = song_element.text
        if(song_title != song_name):
            data_change[0] = True
        song_name = song_title
    except:
        print("error getting song title")
    try:
        artist_element = driver.find_element_by_xpath('//*[@id="layout"]/ytmusic-player-bar/div/div[2]/div[1]/span/span[2]/yt-formatted-string/a[1]')
        artist_title = artist_element.text
        if(artist_title != artist):
            data_change[1] = True
        artist = artist_title
    except:
        print("error getting artist")
    try:
        album_element = driver.find_element_by_xpath('//*[@id="layout"]/ytmusic-player-bar/div/div[2]/div[1]/span/span[2]/yt-formatted-string/a[2]')
        album_title = album_element.text
        if(album_title != album):
            data_change[2] = True
        album = album_title
    except:
        print("error getting album title")
    try:
        year_element = driver.find_element_by_xpath('//*[@id="layout"]/ytmusic-player-bar/div/div[2]/div[1]/span/span[2]/yt-formatted-string')
        year_title = year_element.text
        year_title = year_title[year_title.rfind(" ")+1:]
        if(year_title != year):
            data_change[3] = True
        year = year_title
    except:
        print("error getting year")
    try:
        if(all(data_change) or data_change[0]):
            print(song_name)
            print(artist)
            print(album)
            print(year)
            print()
            data_change = [False]*4
    except:
        pass
        
        
    
                

#driver.exit()


