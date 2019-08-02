import time

try:
    from pirc522 import RFID
except ImportError:
    print("Cannot find library.")

USYD_KEY = []

class Scanner:
    """Class for interacting with the RFID reader"""
    def __init__(self, logger):
        self.rdr = RFID()
        self.logger = logger
        self.util = self.rdr.util()
        self.util.debug = True
        self.last_sid = 0
        self.last_time = 0

    def scan_card(self, key, sector):
        """Attempt to scan a card with a particular key and sector"""
        self.rdr.wait_for_tag()
        (error, _) = self.rdr.request()
        if error:
            self.logger.warn("Could not request tag")
            return True, None
        self.logger.silly("Tag found")
        (error, uid) = self.rdr.anticoll()
        if error:
            self.logger.warn("Error in anticollision")
            return True, None
        self.logger.silly("UID:", uid)
        if self.rdr.select_tag(uid):
            self.logger.warn("Could not select tag")
            return True, None
        self.logger.silly("Selected tag")
        if key is None:
            return self.rdr.read(sector)
        if self.rdr.card_auth(self.rdr.auth_a, sector, key, uid):
            self.logger.warn("Could not authenticate")
            self.rdr.stop_crypto()
            return True, None
        self.logger.silly("Authenticated")
        return self.rdr.read(sector)

    def scan(self):
        """Attempt to scan a student card

        Returns None if no card can be scanned.
        """

        error, data = self.scan_card(USYD_KEY, 12)
        if error:
            return None
        sid = ''.join([chr(x) for x in data]).strip()
        self.logger.info("Found SID:", sid)
        if sid and (sid != self.last_sid or time.time() - self.last_time > 3):
            self.last_sid = sid
            self.last_time = time.time()
            self.rdr.stop_crypto()
            self.logger.buzzer.success()
            return sid
        self.logger.warn("Scan collision")
