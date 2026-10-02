def simplify(x, n):
    """
    Simplify the expression x * n.
    Returns True if x * n evaluates to a whole number, False otherwise.
    
    Both x and n are string representations of fractions in the format <numerator>/<denominator>.
    """
    # Parse x
    x_num, x_den = map(int, x.split('/'))
    # Parse n
    n_num, n_den = map(int, n.split('/'))
    
    # Compute x * n = (x_num * n_num) / (x_den * n_den)
    numerator = x_num * n_num
    denominator = x_den * n_den
    
    # Check if the result is a whole number
    # i.e., numerator % denominator == 0
    return numerator % denominator == 0
