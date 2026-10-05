def encode(message):
    """
    Write a function that takes a message, and encodes in such a 
    way that it swaps case of all letters, replaces all vowels in 
    the message with the letter that appears 2 places ahead of that 
    vowel in the english alphabet. 
    Assume only letters. 
    
    Examples:
    >>> encode('test')
    'TGST'
    >>> encode('This is a message')
    'tHKS KS C MGSSCGG'
    """
    vowels = 'aeiouAEIOU'
    result = []
    for char in message:
        if char in vowels:
            # Replace vowel with letter 2 places ahead
            if char.islower():
                # Lowercase vowel
                base = ord(char)
                new_char = chr(base + 2)
                # Swap case: make it uppercase
                new_char = new_char.upper()
            else:
                # Uppercase vowel
                base = ord(char)
                new_char = chr(base + 2)
                # Swap case: make it lowercase
                new_char = new_char.lower()
            result.append(new_char)
        else:
            # Swap case for non-vowel letters
            if char.isupper():
                result.append(char.lower())
            elif char.islower():
                result.append(char.upper())
            else:
                # Non-letter character, keep as is
                result.append(char)
    return ''.join(result)
