def count_nums(arr):
    """
    Write a function count_nums which takes an array of integers and returns
    the number of elements which has a sum of digits > 0.
    If a number is negative, then its first signed digit will be negative:
    e.g. -123 has signed digits -1, 2, and 3.
    """
    count = 0
    for num in arr:
        s_num = str(num)
        digit_sum = 0
        
        if s_num[0] == '-':
            # First digit is negative, others are positive
            # Handle case where num is just '-' (though not possible for int)
            # and case where num is -0
            first_digit = int(s_num[1])
            digit_sum += -first_digit
            for char in s_num[2:]:
                digit_sum += int(char)
        else:
            # All digits are positive
            for char in s_num:
                digit_sum += int(char)
                
        if digit_sum > 0:
            count += 1
            
    return count
