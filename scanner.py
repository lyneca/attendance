import time

try:
    from pirc522 import RFID
except ImportError:
    print("Cannot find library.")

class Scanner:
    """Class for interacting with the RFID reader"""
    def __init__(self, config, logger):
        with open("/home/pi/usyd_key") as key_file:
            self.key = [ord(x) for x in key_file.read().strip()]
        self.config_key = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]
        self.config = config
        self.rdr = RFID()
        self.logger = logger
        self.util = self.rdr.util()
        self.util.debug = False
        self.last_sid = 0
        self.last_time = 0

    def decode(self, data):
        return ''.join([chr(x) for x in data])

    def decode_number(self, data):
        return int(self.decode(data), 16)

    def wait(self):
        self.rdr.wait_for_tag()

    def request_tag(self):
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
        self.util.set_tag(uid)
        self.logger.silly("Selected tag")
        return False, uid

    def scan_sid(self, uid):
        if self.rdr.card_auth(self.rdr.auth_a, 12, self.key, uid):
            self.logger.warn("Could not authenticate")
            self.rdr.stop_crypto()
            return True, None
        self.logger.silly("Authenticated")
        err, data = self.rdr.read(12)
        return False, self.decode(data).strip()

    def is_config_card(self, uid):
        if self.rdr.card_auth(self.rdr.auth_a, 1, self.config_key, uid):
            self.logger.warn("Could not authenticate")
            self.rdr.stop_crypto()
            return False
        err, data = self.rdr.read(1)
        if err:
            self.logger.warn("Couldn't read data from card")
            return False
        data = self.decode(data).strip()
        return data == "CONFIG CARD"

    def set_config(self, uid):
        self.util.auth(self.rdr.auth_a, self.config_key)
        self.util.do_auth(2)
        err, block_one = self.rdr.read(2)
        if err:
            self.logger.error("Couldn't read data from card")
            return

        course_name = self.decode(block_one[:8])
        course_id = self.decode_number(block_one[8:12])
        token_a = self.decode_number(block_one[12:])

        token_b = []

        for block in [4, 5, 6, 8]:
            self.util.do_auth(block)
            err, data = self.rdr.read(block)
            if err:
                print("Error", data)
                continue
            token_b.append(self.decode(data))
        token = f"{token_a}~{''.join(token_b)}"

        self.config.course_id = course_id
        self.config.course_name = course_name
        self.config.access_token = token
        self.config.ready = True
        self.logger.info(f"Set {course_name} as course")
        self.logger.buzzer.set_config()
        #  self.config.save()


    def scan(self):
        """Attempt to scan a student card

        Returns:
            True, None: if no card can be scanned.
            False, True: If a config card was scanned
            False, [sid]: If a student card can be scanned
        """

        err, uid = self.request_tag()
        if err:
            return True, None
        if self.is_config_card(uid):
            self.set_config(uid)
            return False, True
        else:
            if not self.config.ready:
                self.logger.warn("No configuration selected.")
                self.logger.buzzer.setup_error()
                time.sleep(1)
                return True, None
            err, sid = self.scan_sid(uid)
            if err:
                self.logger.buzzer.error()
                return True, None
            self.logger.info("Found SID:", sid)
            if sid and (sid != self.last_sid or time.time() - self.last_time > 3):
                self.last_sid = sid
                self.last_time = time.time()
                self.rdr.stop_crypto()
                self.logger.buzzer.success()
                return False, sid
            self.logger.warn("Scan collision")
            return True, None
