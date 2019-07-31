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

"""

import sys

from scanner import Scanner
from handler import Handler
from config import Config
from logger import *


def main():
    """Main setup and loop"""
    config = Config(sys.argv[1])
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
