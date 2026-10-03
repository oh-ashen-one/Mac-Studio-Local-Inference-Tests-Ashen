def triples_sum_to_zero(l: list):
    """
    triples_sum_to_zero takes a list of integers as an input.
    it returns True if there are three distinct elements in the list that
    sum to zero, and False otherwise.
    """
    n = len(l)
    if n < 3:
        return False
    
    # Sort the list to use the two-pointer approach
    nums = sorted(l)
    
    for i in range(n - 2):
        # Optimization: if the smallest number is > 0, no triple can sum to 0
        if nums[i] > 0:
            break
            
        left = i + 1
        right = n - 1
        
        while left < right:
            current_sum = nums[i] + nums[left] + nums[right]
            if current_sum == 0:
                return True
            elif current_sum < 0:
                left += 1
            else:
                right -= 1
                
    return False
