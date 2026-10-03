def check_if_last_char_is_a_letter(txt):
    '''
    Create a function that returns True if the last character
    of a given string is an alphabetical character and is not
    a part of a word, and False otherwise.
    Note: "word" is a group of characters separated by space.
    '''
    if not txt or not txt[-1].isalpha():
        return False
    
    # The last character is a letter. 
    # It is "not part of a word" if it is preceded by a space 
    # or if it is the only character in the string.
    if len(txt) == 1:
        return True
    
    return txt[-2] == ' '
