def compare_one(a, b):
    """
    Create a function that takes integers, floats, or strings representing
    real numbers, and returns the larger variable in its given variable type.
    Return None if the values are equal.
    Note: If a real number is represented as a string, the floating point might be . or ,
    """
    def parse_value(x):
        if isinstance(x, (int, float)):
            return float(x)
        if isinstance(x, str):
            x = x.replace(',', '.')
            try:
                return float(x)
            except ValueError:
                return float('nan')
        return float('nan')

    a_val = parse_value(a)
    b_val = parse_value(b)

    if a_val == b_val:
        return None
    return a if a_val > b_val else b
