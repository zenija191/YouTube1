import re

def sanitize(name: str) -> str:
    name = re.sub(r'[^\w\s\-.(),]', '', name.strip())
    return re.sub(r'\s+', '_', name)[:220]

def c(code): return f"\033[{code}m"
G = c(32)   # green
Y = c(33)   # yellow
R = c(31)   # red
RST = c(0)
