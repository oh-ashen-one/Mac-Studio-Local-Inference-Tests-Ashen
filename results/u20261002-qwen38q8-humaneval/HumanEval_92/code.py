def any_int(x, y, z):
    # Check if all three are integers
    if not all(isinstance(n, int) for n in (x, y, z)):
        return False
    
    # Check if one number equals the sum of the other two
    return (x == y + z) or (y == x + z) or (z == x + y)
