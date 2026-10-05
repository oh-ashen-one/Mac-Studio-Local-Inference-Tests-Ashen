def compare_one(a, b):
    """
    Create a function that takes integers, floats, or strings representing
    real numbers, and returns the larger variable in its given variable type.
    Return None if the values are equal.
    Note: If a real number is represented as a string, the floating point might be . or ,

    compare_one(1, 2.5) ➞ 2.5
    compare_one(1, "2,3") ➞ "2,3"
    compare_one("5,1", "6") ➞ "6"
    compare_one("1", 1) ➞ None
    """
    def parse_value(val):
        """Parse a value (int, float, or string) into a float for comparison."""
        if isinstance(val, str):
            # Replace comma with dot for parsing
            normalized = val.replace(',', '.')
            return float(normalized)
        else:
            return float(val)
    
    val_a = parse_value(a)
    val_b = parse_value(b)
    
    if val_a > val_b:
        return a
    elif val_b > val_a:
        return b
    else:
        return None
