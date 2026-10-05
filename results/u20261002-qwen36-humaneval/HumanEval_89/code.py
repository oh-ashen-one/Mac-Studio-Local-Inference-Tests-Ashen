def encrypt(s):
    """Create a function encrypt that takes a string as an argument and
    returns a string encrypted with the alphabet being rotated. 
    The alphabet should be rotated in a manner such that the letters 
    shift down by two multiplied to two places.
    For example:
    encrypt('hi') returns 'lm'
    encrypt('asdfghjkl') returns 'ewhjklnop'
    encrypt('gf') returns 'kj'
    encrypt('et') returns 'ix'
    """
    result = []
    for char in s:
        if char.islower():
            # Shift down by 4 (2 * 2)
            shifted = (ord(char) - ord('a') + 4) % 26 + ord('a')
            result.append(chr(shifted))
        elif char.isupper():
            # Shift down by 4 (2 * 2)
            shifted = (ord(char) - ord('A') + 4) % 26 + ord('A')
            result.append(chr(shifted))
        else:
            # Non-alphabetic characters remain unchanged
            result.append(char)
    return ''.join(result)
