def is_nested(string):
    '''
    Create a function that takes a string as input which contains only square brackets.
    The function should return True if and only if there is a valid subsequence of brackets 
    where at least one bracket in the subsequence is nested.
    '''
    stack = []
    max_depth = 0
    current_depth = 0
    
    for char in string:
        if char == '[':
            stack.append(char)
            current_depth += 1
        elif char == ']':
            if stack:
                stack.pop()
                # A pair is closed. If the depth was > 1 when we opened this, 
                # it means this pair is nested inside another.
                if current_depth > 1:
                    max_depth = max(max_depth, current_depth)
                current_depth -= 1
            else:
                # Reset depth on invalid closing bracket to handle 
                # disjoint valid subsequences
                current_depth = 0
                
    # The problem asks if there is a valid subsequence that is nested.
    # A valid nested structure must reach a depth of at least 2.
    # However, the logic above tracks depth. If we ever closed a bracket 
    # while current_depth was > 1, we found a nested pair.
    
    # Let's refine: a valid nested subsequence exists if we can find " [ [ ] ] " 
    # or " [ [ ] [ ] ] ". This happens if we encounter ']' while the stack size is >= 2.
    
    stack = []
    for char in string:
        if char == '[':
            stack.append(char)
        elif char == ']':
            if len(stack) >= 2:
                return True
            if stack:
                stack.pop()
                
    return False
