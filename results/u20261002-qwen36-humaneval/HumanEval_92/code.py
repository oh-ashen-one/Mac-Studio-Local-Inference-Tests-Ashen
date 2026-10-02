def any_int(x, y, z):
    '''
    Create a function that takes 3 numbers.
    Returns true if one of the numbers is equal to the sum of the other two, and all numbers are integers.
    Returns false in any other cases.
    
    Examples
    any_int(5, 2, 7) ➞ True
    
    any_int(3, 2, 2) ➞ False

    any_int(3, -2, 1) ➞ True
    
    any_int(3.6, -2.2, 2) ➞ False
  
    
    '''
    # Check if all numbers are integers
    for val in (x, y, z):
        if not isinstance(val, int):
            return False
    
    # Check if one number is the sum of the other two
    if x == y + z:
        return True
    if y == x + z:
        return True
    if z == x + y:
        return True
    
    return False
