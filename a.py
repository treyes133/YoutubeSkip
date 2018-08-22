from threading import Thread
import keyboard
class press_detect(Thread):
    

    key = False
    key_combo = keyboard.get_hotkey_name(['ctrl','alt','n'])
    status = True
    def __init__(self):
        Thread.__init__(self)
    def run(self):
        keyboard.add_hotkey(self.key_combo, self.val)
        while self.status is True:
            if(self.key is True):
                print("Hello!")
                self.key = False

    def val(self):
        self.key = True
    
    
pd = press_detect()
pd.start()
