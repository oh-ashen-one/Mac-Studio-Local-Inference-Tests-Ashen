def check_if_last_char_is_a_letter(txt):
    '''
    Create a function that returns True if the last character
    of a given string is an alphabetical character and is not
    a part of a word, and False otherwise.
    Note: "word" is a group of characters separated by space.

    Examples:
    check_if_last_char_is_a_letter("apple pie") ➞ False
    check_if_last_char_is_a_letter("apple pi e") ➞ True
    check_if_last_char_is_a_letter("apple pi e ") ➞ False
    check_if_last_char_is_a_letter("") ➞ False 
    '''
    if not txt:
        return False
    
    # Strip trailing spaces
    stripped = txt.rstrip()
    if not stripped:
        return False
    
    # Get the last character
    last_char = stripped[-1]
    
    # Check if it's an alphabetical character
    if not last_char.isalpha():
        return False
    
    # Check if the last character is not part of a word
    # A word is a group of characters separated by space.
    # If the last character is part of a word, then the character before it
    # (if exists) should be a letter (or part of the same word).
    # If the last character is standalone (not part of a word), then either:
    #   - The string has only one character, OR
    #   - The character before the last character is a space.
    
    if len(stripped) == 1:
        return True
    
    # Check the character before the last character
    prev_char = stripped[-2]
    
    # If the previous character is a space, then the last character is standalone
    if prev_char == ' ':
        return True
    else:
        # The last character is part of a word
        return False
