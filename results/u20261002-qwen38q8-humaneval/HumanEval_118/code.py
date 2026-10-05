def get_closest_vowel(word):
    """You are given a word. Your task is to find the closest vowel that stands between 
    two consonants from the right side of the word (case sensitive).
    
    Vowels in the beginning and ending doesn't count. Return empty string if you didn't
    find any vowel met the above condition. 

    You may assume that the given string contains English letter only.

    Example:
    get_closest_vowel("yogurt") ==> "u"
    get_closest_vowel("FULL") ==> "U"
    get_closest_vowel("quick") ==> ""
    get_closest_vowel("ab") ==> ""
    """
    vowels = set('aeiouAEIOU')
    
    # We need to find a vowel that is between two consonants
    # "from the right side" means we start checking from the right
    # Vowels at the beginning (index 0) and ending (last index) don't count
    
    n = len(word)
    if n < 3:
        return ""
    
    # Iterate from right to left, starting from index n-2 down to 1
    # (index 0 and n-1 are excluded as they are beginning and ending)
    for i in range(n - 2, 0, -1):
        if word[i] in vowels:
            # Check if both neighbors are consonants
            left_char = word[i - 1]
            right_char = word[i + 1]
            
            # A consonant is a letter that is not a vowel
            if left_char not in vowels and right_char not in vowels:
                return word[i]
    
    return ""
