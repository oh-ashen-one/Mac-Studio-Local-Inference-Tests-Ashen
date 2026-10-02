def unique_digits(x):
    """Given a list of positive integers x. return a sorted list of all 
    elements that hasn't any even digit.

    Note: Returned list should be sorted in increasing order.
    
    For example:
    >>> unique_digits([15, 33, 1422, 1])
    [1, 15, 33]
    >>> unique_digits([152, 323, 1422, 10])
    []
    """
    result = []
    even_digits = {'0', '2', '4', '6', '8'}
    for num in x:
        s_num = str(num)
        if not any(digit in even_digits for digit in s_num):
            result.append(num)
    return sorted(result)
