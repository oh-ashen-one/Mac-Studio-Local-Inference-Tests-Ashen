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
    
    # Sort by: 1) descending unique char count, 2) ascending lexicographical order
    # Python's sort is stable, so we sort by lexicographical first, then by unique count
    sorted_words = sorted(words, key=lambda w: (-len(set(w)), w))
    return sorted_words[0]
