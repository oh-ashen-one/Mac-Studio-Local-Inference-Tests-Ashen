def encode(message):
    """
    Write a function that takes a message, and encodes in such a 
    way that it swaps case of all letters, replaces all vowels in 
    the message with the letter that appears 2 places ahead of that 
    vowel in the english alphabet. 
    Assume only letters. 
    """
    vowels = "aeiouAEIOU"
    result = []
    
    for char in message:
        if char == ' ':
            result.append(' ')
            continue
            
        # Swap case
        swapped = char.swapcase()
        
        # Check if the original character was a vowel
        if char in vowels:
            # Shift the swapped character by 2 places in the alphabet
            # We use the swapped character's case for the shift
            shifted_char = chr(ord(swapped) + 2)
            result.append(shifted_char)
        else:
            result.append(swapped)
            
    return "".join(result)
