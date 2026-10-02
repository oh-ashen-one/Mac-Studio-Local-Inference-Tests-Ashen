import re

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
    # Split the string into sentences using '.', '?', or '!' as delimiters
    # We need to split on these characters but keep track of sentence boundaries
    # Use regex to split on sentence-ending punctuation
    sentences = re.split(r'[.!?]', S)
    
    count = 0
    for sentence in sentences:
        # Strip leading/trailing whitespace
        stripped = sentence.strip()
        if not stripped:
            continue
        # Check if the sentence starts with "I"
        # The sentence should start with the word "I"
        # Split into words and check if the first word is "I"
        words = stripped.split()
        if words and words[0] == "I":
            count += 1
    
    return count
