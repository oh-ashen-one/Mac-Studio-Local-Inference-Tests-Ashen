def find_max(words):
    """Write a function that accepts a list of strings.
    The list contains different words. Return the word with maximum number
    of unique characters. If multiple strings have maximum number of unique
    characters, return the one which comes first in lexicographical order.
    """
    if not words:
        return ""
    
    # We want to maximize the number of unique characters.
    # In case of a tie, we want the lexicographically smallest word.
    # max() returns the first occurrence in case of a tie.
    # To handle the lexicographical tie-break, we can use a key that 
    # returns (unique_count, negative_lexicographical_order) or 
    # simply sort the list lexicographically first.
    
    # Sort words lexicographically first to ensure the first one encountered 
    # by max() is the lexicographically smallest.
    sorted_words = sorted(words)
    
    return max(sorted_words, key=lambda w: len(set(w)))
