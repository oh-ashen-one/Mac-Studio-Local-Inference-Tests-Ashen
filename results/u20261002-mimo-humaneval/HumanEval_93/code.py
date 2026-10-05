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
    vowels = "aeiouAEIOU"
    result = []
    for char in message:
        if char in vowels:
            # Swap case first
            swapped = char.swapcase()
            # Find the position in the alphabet (0-25)
            pos = ord(swapped.lower()) - ord('a')
            # Shift by 2
            new_pos = (pos + 2) % 26
            # Get the new letter, preserving the swapped case
            new_char = chr(ord('a') + new_pos)
            if swapped.isupper():
                new_char = new_char.upper()
            result.append(new_char)
        else:
            result.append(char.swapcase())
    return ''.join(result)
