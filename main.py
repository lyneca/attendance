"""
1. Configuration
  - Get data from Firebase
    - Server, course code
    - Access token
    - Encrypted?
2. Scanning
  - Feedback
3. Sending
  - Asynchronous

Error Codes

- Setup
  - No internet
  - Can't authenticate
  - No assignment found

"""

from time import sleep

from scanner import Scanner
from handler import Handler
from config import Config
from logger import Logger
from buzzer import Buzzer


def main():
    """Main setup and loop"""
    buzzer = Buzzer()
    logger = Logger(buzzer, 1)

    logger.info("Initialising reader")

    config = Config(logger)

    #  err = True
    #  while err:
        #  err = config.update_config()
        #  sleep(3)

    scanner = Scanner(config, logger)

    handler = Handler(logger, config)

    handler.get_assignments()

    buzzer.setup_complete()

    logger.info("Ready")

    while True:
        data = scanner.scan()
        if data is None:
            continue
        handler.send(data)

if __name__ == '__main__':
    main()
