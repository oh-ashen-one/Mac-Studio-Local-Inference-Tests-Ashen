def move_one_ball(arr):
    """We have an array 'arr' of N integers arr[1], arr[2], ..., arr[N].The
    numbers in the array will be randomly ordered. Your task is to determine if
    it is possible to get an array sorted in non-decreasing order by performing 
    the following operation on the given array:
        You are allowed to perform right shift operation any number of times.
    
    One right shift operation means shifting all elements of the array by one
    position in the right direction. The last element of the array will be moved to
    the starting position in the array i.e. 0th index. 

    If it is possible to obtain the sorted array by performing the above operation
    then return True else return False.
    If the given array is empty then return True.

    Note: The given list is guaranteed to have unique elements.
    """
    if not arr:
        return True
    
    n = len(arr)
    # A right-shifted sorted array will have at most one point where arr[i] > arr[i+1]
    # If it has exactly one such point, the last element must be less than or equal to the first element.
    # If it has zero such points, it is already sorted.
    
    count_drops = 0
    for i in range(n - 1):
        if arr[i] > arr[i + 1]:
            count_drops += 1
            
    if count_drops == 0:
        return True
    if count_drops == 1:
        # Check if the wrap-around is also non-decreasing
        return arr[n - 1] <= arr[0]
        
    return False
