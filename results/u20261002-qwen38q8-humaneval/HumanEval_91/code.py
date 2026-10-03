def is_bored(S):
    """
    You'll be given a string of words, and your task is to count the number
    of boredoms. A boredom is a sentence that starts with the word "I".
    Sentences are delimited by '.', '?' or '!'.
   
    For example:
    >>> is_bored("Hello world")
    0
    >>> is_bored("The sky is blue. The sun is shining. I love this weather")
    1
    """
    import re
    
    # Split the string into sentences by '.', '?' or '!'
    # We need to handle the case where the last sentence might not end with a delimiter
    sentences = re.split(r'[.?!]', S)
    
    count = 0
    for sentence in sentences:
        # Strip whitespace from the sentence
        stripped = sentence.strip()
        if not stripped:
            continue
        # Check if the sentence starts with the word "I"
        # We need to make sure it's the word "I" and not part of another word
        # Split into words and check the first word
        words = stripped.split()
        if words and words[0] == "I":
            count += 1
    
    return count
