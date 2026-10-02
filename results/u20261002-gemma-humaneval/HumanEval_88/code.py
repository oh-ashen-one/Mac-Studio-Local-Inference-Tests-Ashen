def sort_array(array):
    """
    Given an array of non-negative integers, return a copy of the given array after sorting,
    you will sort the given array in ascending order if the sum( first index value, last index value) is odd,
    or sort it in descending order if the sum( first index value, last index value) is even.

    Note:
    * don't change the given array.
    """
    if not array:
        return []
    
    # Calculate sum of first and last index values
    first_val = array[0]
    last_val = array[-1]
    total_sum = first_val + last_val
    
    # Determine sorting order based on parity of the sum
    # Odd -> Ascending (reverse=False), Even -> Descending (reverse=True)
    is_descending = (total_sum % 2 == 0)
    
    return sorted(array, reverse=is_descending)
