def select_words(s, n):
    """Given a string s and a natural number n, you have been tasked to implement 
    a function that returns a list of all words from string s that contain exactly 
    n consonants, in order these words appear in the string s.
    If the string s is empty then the function should return an empty list.
    Note: you may assume the input string contains only letters and spaces.
    """
    if not s:
        return []
    
    vowels = "aeiouAEIOU"
    words = s.split()
    result = []
    
    for word in words:
        consonant_count = 0
        for char in word:
            if char.isalpha() and char not in vowels:
                consonant_count += 1
        
        if consonant_count == n:
            result.append(word)
            
    return result
