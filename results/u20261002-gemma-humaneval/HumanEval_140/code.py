import re

def fix_spaces(text):
    """
    Given a string text, replace all spaces in it with underscores, 
    and if a string has more than 2 consecutive spaces, 
    then replace all consecutive spaces with - 
    """
    # First, handle sequences of 3 or more spaces
    text = re.sub(r' {3,}', '-', text)
    # Then, handle remaining single or double spaces
    text = text.replace(' ', '_')
    return text
