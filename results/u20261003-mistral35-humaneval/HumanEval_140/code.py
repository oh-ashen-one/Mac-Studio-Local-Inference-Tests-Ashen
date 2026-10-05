import re

def fix_spaces(text):
    """
    Given a string text, replace all spaces in it with underscores,
    and if a string has more than 2 consecutive spaces,
    then replace all consecutive spaces with -
    """
    # Replace sequences of 3 or more spaces with a single '-'
    text = re.sub(r' {3,}', '-', text)
    # Replace remaining single or double spaces with underscores
    text = re.sub(r' {1,2}', '_', text)
    return text
