def change_base(x: int, base: int):
    """Change numerical base of input number x to base.
    return string representation after the conversion.
    base numbers are less than 10.
    >>> change_base(8, 3)
    '22'
    >>> change_base(8, 2)
    '1000'
    >>> change_base(7, 2)
    '111'
    """
    if x == 0:
        return '0'
    
    negative = False
    if x < 0:
        negative = True
        x = -x
    
    digits = []
    while x > 0:
        digits.append(str(x % base))
        x //= base
    
    result = ''.join(reversed(digits))
    if negative:
        result = '-' + result
    
    return result
