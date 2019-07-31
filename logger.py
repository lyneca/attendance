def print_prefix(code, *msg):
    print(f"[{code: >5}]", *msg)

def info(*msg):
    """Log an info message"""
    print_prefix("INFO", *msg)

def warn(*msg):
    """Log a warning message"""
    print_prefix("WARN", *msg)

def error(*msg):
    """Log an error message"""
    print_prefix("ERROR", *msg)