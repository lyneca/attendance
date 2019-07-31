import logger

try:
    from pirc522 import RFID
except ImportError:
    print("Cannot find library.")

KEY = []

class Scanner:
    def __init__(self):
        ...

    def scan(self):
        """Attempt to scan a card

        Returns None if no card can be scanned.
        """
        if False:
            return True
        return None

