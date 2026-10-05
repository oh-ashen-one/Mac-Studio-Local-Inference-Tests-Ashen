def get_closest_vowel(word):
    """You are given a word. Your task is to find the closest vowel that stands between 
    two consonants from the right side of the word (case sensitive).
    
    Vowels in the beginning and ending doesn't count. Return empty string if you didn't
    find any vowel met the above condition. 

    You may assume that the given string contains English letter only.
    """
    vowels = "aeiouAEIOU"
    # Iterate from the second to last character back to the second character
    for i in range(len(word) - 2, 0, -1):
        char = word[i]
        if char in vowels:
            # Check if the character is surrounded by consonants
            # A consonant is any letter that is not a vowel
            if word[i-1] not in vowels and word[i+1] not in vowels:
                return char
    return ""
