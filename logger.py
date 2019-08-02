def print_prefix(self, code, *msg):
    """Print a message with a prefix"""
    print("[{: >4}]".format(code), *msg)

class Logger:
    """Class for handling logging"""
    def __init__(self, buzzer, level=1):
        self.buzzer = buzzer
        self.level = level

    def silly(self, *msg):
        """Log a silly-level message"""
        if self.level > 0:
            return
        print_prefix("SILL", *msg)

    def info(self, *msg):
        """Log an info message"""
        if self.level > 1:
            return
        print_prefix("INFO", *msg)

    def warn(self, *msg):
        """Log a warning message"""
        if self.level > 2:
            return
        print_prefix("WARN", *msg)

    def error(self, *msg):
        """Log an error message"""
        if self.level > 3:
            return
        print_prefix("ERR", *msg)
