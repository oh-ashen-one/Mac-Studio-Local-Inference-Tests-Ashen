def count_nums(arr):
    """
    Write a function count_nums which takes an array of integers and returns
    the number of elements which has a sum of digits > 0.
    If a number is negative, then its first signed digit will be negative:
    e.g. -123 has signed digits -1, 2, and 3.
    >>> count_nums([]) == 0
    >>> count_nums([-1, 11, -11]) == 1
    >>> count_nums([1, 1, 2]) == 3
    """
    count = 0
    for num in arr:
        if num == 0:
            # Sum of digits of 0 is 0, which is not > 0
            continue
        if num < 0:
            # For negative numbers, the first digit is negative
            s = str(num)
            # Remove the '-' sign
            digits_str = s[1:]
            # First digit is negative, rest are positive
            first_digit = -int(digits_str[0])
            rest_sum = sum(int(d) for d in digits_str[1:])
            total = first_digit + rest_sum
        else:
            s = str(num)
            total = sum(int(d) for d in s)
        if total > 0:
            count += 1
    return count
