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
import logger


def main():
    """Main setup and loop"""
    logger.info("Initialising reader")
    config = Config()
    config.update_config()
    scanner = Scanner()
    handler = Handler(config)
    while True:
        data = scanner.scan()
        if data is None:
            continue
        handler.send(data)

if __name__ == '__main__':
    main()
