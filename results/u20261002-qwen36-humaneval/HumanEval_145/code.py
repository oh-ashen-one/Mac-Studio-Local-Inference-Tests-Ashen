def order_by_points(nums):
    """
    Write a function which sorts the given list of integers
    in ascending order according to the sum of their digits.
    Note: if there are several items with similar sum of their digits,
    order them based on their index in original list.

    For example:
    >>> order_by_points([1, 11, -1, -11, -12]) == [-1, -11, 1, -12, 11]
    >>> order_by_points([]) == []
    """
    def digit_sum(n):
        """Calculate the sum of digits of an integer, treating negative sign separately."""
        s = str(n)
        if s[0] == '-':
            # For negative numbers, sum the digits of the absolute value
            return sum(int(c) for c in s[1:])
        else:
            return sum(int(c) for c in s)
    
    # Sort by (digit_sum, original_index)
    indexed = [(num, i) for i, num in enumerate(nums)]
    indexed.sort(key=lambda x: (digit_sum(x[0]), x[1]))
    return [num for num, _ in indexed]
