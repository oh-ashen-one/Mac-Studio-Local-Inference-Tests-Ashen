def sort_array(array):
    """
    Given an array of non-negative integers, return a copy of the given array after sorting,
    you will sort the given array in ascending order if the sum( first index value, last index value) is odd,
    or sort it in descending order if the sum( first index value, last index value) is even.

    Note:
    * don't change the given array.

    Examples:
    * sort_array([]) => []
    * sort_array([5]) => [5]
    * sort_array([2, 4, 3, 0, 1, 5]) => [0, 1, 2, 3, 4, 5]
    * sort_array([2, 4, 3, 0, 1, 5, 6]) => [6, 5, 4, 3, 2, 1, 0]
    """
    if not array:
        return []
    
    # Get first and last index values (i.e., the values at index 0 and index len-1)
    first_val = array[0]
    last_val = array[-1]
    total = first_val + last_val
    
    # Create a copy of the array
    sorted_array = list(array)
    
    if total % 2 == 1:
        # Odd sum: sort in ascending order
        sorted_array.sort()
    else:
        # Even sum: sort in descending order
        sorted_array.sort(reverse=True)
    
    return sorted_array
