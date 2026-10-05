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
    if len(word) < 3:
        return ""
    
    vowels = set('aeiouAEIOU')
    
    # Traverse from right to left, looking for a vowel that is between two consonants
    # We need to find the closest vowel (from the right) that has consonants on both sides
    
    # Let's iterate from the second-to-last character down to index 1
    # For each position i, check if word[i] is a vowel, and word[i-1] and word[i+1] are consonants
    
    for i in range(len(word) - 2, 0, -1):
        if word[i] in vowels:
            # Check if both neighbors are consonants
            if word[i - 1] not in vowels and word[i + 1] not in vowels:
                return word[i]
    
    return ""
