def order_by_points(nums):
    """
    Write a function which sorts the given list of integers
    in ascending order according to the sum of their digits.
    Note: if there are several items with similar sum of their digits,
    order them based on their index in original list.
    """
    def digit_sum(n):
        return sum(int(d) for d in str(abs(n)))

    indexed_nums = [(digit_sum(num), idx, num) for idx, num in enumerate(nums)]
    indexed_nums.sort(key=lambda x: (x[0], x[1]))
    return [num for (_, _, num) in indexed_nums]
