def order_by_points(nums):
    """
    Write a function which sorts the given list of integers
    in ascending order according to the sum of their digits.
    Note: if there are several items with similar sum of their digits,
    order them based on their index in original list.
    """
    def get_digit_sum(n):
        # Use absolute value to handle negative numbers
        return sum(int(digit) for digit in str(abs(n)))

    # Python's sort is stable, so sorting by digit sum alone 
    # preserves the original relative order of elements with the same sum.
    return sorted(nums, key=get_digit_sum)
