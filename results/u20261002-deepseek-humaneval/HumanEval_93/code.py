def encode(message):
    vowels = 'aeiouAEIOU'
    result = []
    for char in message:
        if char.isalpha():
            if char in vowels:
                new_char = chr(ord(char) + 2)
                if char.islower() and new_char.isupper():
                    new_char = new_char.lower()
                elif char.isupper() and new_char.islower():
                    new_char = new_char.upper()
                result.append(new_char.swapcase())
            else:
                result.append(char.swapcase())
        else:
            result.append(char)
    return ''.join(result)
