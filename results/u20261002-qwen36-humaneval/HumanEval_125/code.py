def split_words(txt):
    '''
    Given a string of words, return a list of words split on whitespace, if no whitespaces exists in the text you
    should split on commas ',' if no commas exists you should return the number of lower-case letters with odd order in the
    alphabet, ord('a') = 0, ord('b') = 1, ... ord('z') = 25
    Examples
    split_words("Hello world!") ➞ ["Hello", "world!"]
    split_words("Hello,world!") ➞ ["Hello", "world!"]
    split_words("abcdef") == 3 
    '''
    # Check if there are whitespaces
    if ' ' in txt or '\t' in txt or '\n' in txt or '\r' in txt or '\f' in txt or '\v' in txt:
        return txt.split()
    
    # Check if there are commas
    if ',' in txt:
        return txt.split(',')
    
    # Count lower-case letters with odd order in the alphabet
    # ord('a') = 0 (even), ord('b') = 1 (odd), ord('c') = 2 (even), ord('d') = 3 (odd), ...
    # So odd order means: b, d, f, h, j, l, n, p, r, t, v, x, z
    count = 0
    for char in txt:
        if 'a' <= char <= 'z':
            ord_val = ord(char) - ord('a')
            if ord_val % 2 == 1:
                count += 1
    return count
