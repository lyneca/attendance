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

Modules

- Configuration
- Scanner
- Handler

Error Codes

- Setup
  - No internet
  - Can't authenticate
  - No assignment found

"""

import sys

from scanner import Scanner
from handler import Handler
from config import Config
from logger import Logger


def main():
    """Main setup and loop"""
    logger = Logger(1)
    logger.info("Initialising reader")
    config = Config(logger)
    config.update_config()
    scanner = Scanner(logger)
    handler = Handler(logger, config)
    handler.get_assignments()
    while True:
        data = scanner.scan()
        if data is None:
            continue
        handler.send(data)

if __name__ == '__main__':
    main()
