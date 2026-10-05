def is_palindrome(string: str) -> bool:
    """ Test if given string is a palindrome """
    return string == string[::-1]


def make_palindrome(string: str) -> str:
    """ Find the shortest palindrome that begins with a supplied string.
    Algorithm idea is simple:
    - Find the longest postfix of supplied string that is a palindrome.
    - Append to the end of the string reverse of a string prefix that comes before the palindromic suffix.
    >>> make_palindrome('')
    ''
    >>> make_palindrome('cat')
    'catac'
    >>> make_palindrome('cata')
    'catac'
    """
    if not string:
        return ''
    
    # Find the longest palindromic suffix
    # We want the longest suffix of `string` that is a palindrome
    # Then we take the prefix before that suffix, reverse it, and append it
    
    n = len(string)
    longest_pal_suffix_len = 0
    
    for i in range(n):
        # Check if string[i:] is a palindrome
        suffix = string[i:]
        if is_palindrome(suffix):
            # This is a palindromic suffix starting at index i
            # The length of this suffix is n - i
            # We want the longest such suffix
            if n - i > longest_pal_suffix_len:
                longest_pal_suffix_len = n - i
    
    # The prefix before the palindromic suffix
    prefix = string[:n - longest_pal_suffix_len]
    # Reverse the prefix and append it
    return string + prefix[::-1]
