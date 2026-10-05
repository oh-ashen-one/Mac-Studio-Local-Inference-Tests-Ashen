def solve(s):
    has_letters = any(c.isalpha() for c in s)
    if not has_letters:
        return s[::-1]
    return ''.join(c.swapcase() if c.isalpha() else c for c in s)
