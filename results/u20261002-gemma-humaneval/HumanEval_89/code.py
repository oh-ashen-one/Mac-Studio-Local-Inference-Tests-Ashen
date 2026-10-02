import string

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
    shift = 2 * 2
    result = []
    for char in s:
        if 'a' <= char <= 'z':
            # Shift lowercase letters
            shifted = chr((ord(char) - ord('a') + shift) % 26 + ord('a'))
            result.append(shifted)
        elif 'A' <= char <= 'Z':
            # Shift uppercase letters
            shifted = chr((ord(char) - ord('A') + shift) % 26 + ord('A'))
            result.append(shifted)
        else:
            # Keep non-alphabetic characters as they are
            result.append(char)
    return "".join(result)
