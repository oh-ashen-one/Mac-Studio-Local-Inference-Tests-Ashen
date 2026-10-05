import re

def is_bored(S):
    """
    You'll be given a string of words, and your task is to count the number
    of boredoms. A boredom is a sentence that starts with the word "I".
    Sentences are delimited by '.', '?' or '!'.
    """
    # Split the string by any of the delimiters '.', '?', or '!'
    sentences = re.split(r'[.?!]', S)
    
    count = 0
    for sentence in sentences:
        # Strip leading whitespace to find the first word
        stripped = sentence.lstrip()
        # Check if the sentence starts with the word "I" followed by a space or end of string
        if stripped.startswith("I") and (len(stripped) == 1 or not stripped[1].isalpha()):
            count += 1
            
    return count
