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

    scanner = Scanner(config, logger)

    buzzer.ready()

    # Loop until either config is successfully downloaded, or a config card is
    #  scanned
    err = True
    while err and not config.ready:
        buzzer.ready()
        err, _ = scanner.scan()
        if err:
            err = config.update_config()

    handler = Handler(logger, config)
    handler.get_assignments()

    logger.info("Ready")

    while True:
        scanner.wait()
        err, data = scanner.scan()
        if err:
            continue
        if data is True:
            handler.get_assignments()
        else:
            handler.send(data)

if __name__ == '__main__':
    main()
