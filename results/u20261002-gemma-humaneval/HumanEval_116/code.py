def sort_array(arr):
    """
    In this Kata, you have to sort an array of non-negative integers according to
    number of ones in their binary representation in ascending order.
    For similar number of ones, sort based on decimal value.
    """
    # bin(x).count('1') counts the set bits.
    # The sort key is a tuple: (number of ones, decimal value).
    # Python's sort is stable, but providing the value as the second element 
    # of the tuple ensures the secondary sort requirement.
    return sorted(arr, key=lambda x: (bin(x).count('1') if x >= 0 else bin(x).count('1'), x))
