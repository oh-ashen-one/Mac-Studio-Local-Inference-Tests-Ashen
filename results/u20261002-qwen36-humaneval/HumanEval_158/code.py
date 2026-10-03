def find_max(words):
    """Write a function that accepts a list of strings.
    The list contains different words. Return the word with maximum number
    of unique characters. If multiple strings have maximum number of unique
    characters, return the one which comes first in lexicographical order.

    find_max(["name", "of", "string"]) == "string"
    find_max(["name", "enam", "game"]) == "enam"
    find_max(["aaaaaaa", "bb" ,"cc"]) == "aaaaaaa"
    """
    if not words:
        return ""
    
    # For each word, compute the number of unique characters
    # Then find the max, and among those with max, pick lexicographically smallest
    
    best_word = None
    max_unique = -1
    
    for word in words:
        unique_count = len(set(word))
        if unique_count > max_unique:
            max_unique = unique_count
            best_word = word
        elif unique_count == max_unique:
            # Pick lexicographically smaller
            if word < best_word:
                best_word = word
    
    return best_word
