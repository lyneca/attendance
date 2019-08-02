class Logger:
    def __init__(self, level=1):
        self.level = level

    def print_prefix(self, code, *msg):
        print("[{: >4}]".format(code), *msg)

    def info(self, *msg):
        """Log an info message"""
        if self.level > 1:
            return
        self.print_prefix("INFO", *msg)

    def warn(self, *msg):
        """Log a warning message"""
        if self.level > 2:
            return
        self.print_prefix("WARN", *msg)

    def error(self, *msg):
        """Log an error message"""
        if self.level > 3:
            return
        self.print_prefix("ERR", *msg)

    def silly(self, *msg):
        if self.level > 0:
            return
        self.print_prefix("SILL", *msg)
