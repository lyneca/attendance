import time

import logger
import buzzer

try:
    from pirc522 import RFID
except ImportError:
    print("Cannot find library.")

KEY = []

class Scanner:
    def __init__(self):
        self.rdr = RFID()
        self.util = self.rdr.util()
        self.util.debug = True
        self.last_sid = 0
        self.last_time = 0


    def scan(self):
        """Attempt to scan a card

        Returns None if no card can be scanned.
        """

        logger.info("Ready.")

        buzzer.setup_complete()

        self.rdr.wait_for_tag()
        (e, tag_type) = self.rdr.request()
        if e:
            logger.error("Could not request tag")
            buzzer.error()
            return
        logger.info("Tag found")
        (e, uid) = self.rdr.anticoll()
        if e:
            logger.error("Error in anticollision")
            buzzer.error()
            return
        logger.info("UID:", uid)
        if self.rdr.select_tag(uid):
            logger.error("Could not select tag")
            buzzer.error()
            return
        logger.info("Selected tag")
        if self.rdr.card_auth(self.rdr.auth_a, 12, KEY, uid):
            logger.error("Could not authenticate")
            buzzer.error()
            self.rdr.stop_crypto()
            return
        logger.info("Authenticated")
        data = self.rdr.read(12)[1]
        sid = ''.join([chr(x) for x in data]).strip()
        logger.info("SID:", sid)
        if sid and sid != last_sid or time.time() - last_time > 3:
            last_sid = sid
            last_time = time.time()
            self.rdr.stop_crypto()
            return sid
        else:
            logger.error("Scan collision")
            buzzer.error()
