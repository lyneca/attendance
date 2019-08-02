import time

import logger
import buzzer

try:
    from pirc522 import RFID
except ImportError:
    print("Cannot find library.")

USYD_KEY = []

class Scanner:
    """Class for interacting with the RFID reader"""
    def __init__(self):
        self.rdr = RFID()
        self.util = self.rdr.util()
        self.util.debug = True
        self.last_sid = 0
        self.last_time = 0

    def scan_card(self, key, sector):
        """Attempt to scan a card with a particular key and sector"""
        self.rdr.wait_for_tag()
        (error, _) = self.rdr.request()
        if error:
            logger.error("Could not request tag")
            buzzer.error()
            return True, None
        logger.info("Tag found")
        (error, uid) = self.rdr.anticoll()
        if error:
            logger.error("Error in anticollision")
            buzzer.error()
            return True, None
        logger.info("UID:", uid)
        if self.rdr.select_tag(uid):
            logger.error("Could not select tag")
            buzzer.error()
            return True, None
        logger.info("Selected tag")
        if key is None:
            return self.rdr.read(sector)
        if self.rdr.card_auth(self.rdr.auth_a, sector, key, uid):
            logger.error("Could not authenticate")
            buzzer.error()
            self.rdr.stop_crypto()
            return True, None
        logger.info("Authenticated")
        return self.rdr.read(sector)

    def scan(self):
        """Attempt to scan a student card

        Returns None if no card can be scanned.
        """

        error, data = self.scan_card(USYD_KEY, 12)
        if error:
            return None
        sid = ''.join([chr(x) for x in data]).strip()
        logger.info("SID:", sid)
        if sid and sid != last_sid or time.time() - last_time > 3:
            last_sid = sid
            last_time = time.time()
            self.rdr.stop_crypto()
            return sid
        logger.error("Scan collision")
        buzzer.error()
