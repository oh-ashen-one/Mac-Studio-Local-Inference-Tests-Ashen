import re

def check_if_last_char_is_a_letter(txt):
    if not txt:
        return False
    last_char = txt[-1]
    if not last_char.isalpha():
        return False
    # Check if the last character is a standalone letter (not part of a word)
    # Split into words and check if the last character is a word by itself
    words = txt.split()
    if not words:
        return False
    return words[-1] == last_char
