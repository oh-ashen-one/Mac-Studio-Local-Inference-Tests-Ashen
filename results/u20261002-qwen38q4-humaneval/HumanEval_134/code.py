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
    
    # The last character must be an alphabetical character
    last_char = txt[-1]
    if not last_char.isalpha():
        return False
    
    # Check if the last character is not part of a word
    # A word is a group of characters separated by space
    # So the last character is not part of a word if it's preceded by a space
    # or if it's the only character (but then it would be a word of length 1)
    
    # Let's think about this more carefully:
    # "apple pi e" -> last char is 'e', preceded by space, so 'e' is a standalone word -> True
    # "apple pie" -> last char is 'e', preceded by 'i', so 'e' is part of "pie" -> False
    # "apple pi e " -> last char is ' ', not alpha -> False
    
    # So the condition is: the last character is alpha AND the character before it is a space
    # OR the string has only one character (which is alpha)
    
    if len(txt) == 1:
        return True
    
    # Check if the character before the last one is a space
    if txt[-2] == ' ':
        return True
    
    return False
