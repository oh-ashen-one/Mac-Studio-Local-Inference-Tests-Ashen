def make_palindrome(string: str) -> str:
    if not string:
        return ""
    
    # Find the longest palindromic suffix
    for i in range(len(string)):
        suffix = string[i:]
        if suffix == suffix[::-1]:
            prefix = string[:i]
            return string + prefix[::-1]
    
    return string  # Should never reach here for valid inputs
