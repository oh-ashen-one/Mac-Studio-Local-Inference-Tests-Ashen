import re

def fix_spaces(text):
    return re.sub(r' {3,}', '-', re.sub(r' ', '_', text))
