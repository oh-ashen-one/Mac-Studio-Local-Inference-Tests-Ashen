def encrypt(s: str) -> str:
    result = []
    for char in s:
        if 'a' <= char <= 'z':
            shifted = chr((ord(char) - ord('a') + 4) % 26 + ord('a'))
        elif 'A' <= char <= 'Z':
            shifted = chr((ord(char) - ord('A') + 4) % 26 + ord('A'))
        else:
            shifted = char
        result.append(shifted)
    return ''.join(result)
