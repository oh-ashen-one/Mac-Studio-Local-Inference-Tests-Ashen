def specialFilter(nums):
    """Write a function that takes an array of numbers as input and returns 
    the number of elements in the array that are greater than 10 and both 
    first and last digits of a number are odd (1, 3, 5, 7, 9).
    For example:
    specialFilter([15, -73, 14, -15]) => 1 
    specialFilter([33, -2, -3, 45, 21, 109]) => 2
    """
    def get_first_and_last_digits(n):
        # Get the absolute value to handle negative numbers
        abs_n = abs(n)
        # Convert to string to get digits
        s = str(abs_n)
        first_digit = int(s[0])
        last_digit = int(s[-1])
        return first_digit, last_digit
    
    def is_odd(digit):
        return digit in [1, 3, 5, 7, 9]
    
    count = 0
    for num in nums:
        # Check if greater than 10
        if num > 10:
            first_digit, last_digit = get_first_and_last_digits(num)
            if is_odd(first_digit) and is_odd(last_digit):
                count += 1
    
    return count
