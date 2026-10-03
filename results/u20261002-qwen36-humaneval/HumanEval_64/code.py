def vowels_count(s: str) -> int:
    """
    Count the number of vowels in a string.
    Vowels are 'a', 'e', 'i', 'o', 'u'.
    'y' is also considered a vowel only when it is at the end of the word.
    
    Args:
        s: A string representing a word.
        
    Returns:
        The number of vowels in the string.
        
    Examples:
        >>> vowels_count("abcde")
        2
        >>> vowels_count("ACEDY")
        3
    """
    if not s:
        return 0
    
    vowels = set('aeiouAEIOU')
    count = 0
    
    for i, char in enumerate(s):
        if char in vowels:
            count += 1
        elif char == 'y' or char == 'Y':
            # 'y' is a vowel only when it is at the end of the word
            if i == len(s) - 1:
                count += 1
    
    return count
