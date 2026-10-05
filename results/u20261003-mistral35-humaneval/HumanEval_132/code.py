def is_nested(string):
    '''
    Create a function that takes a string as input which contains only square brackets.
    The function should return True if and only if there is a valid subsequence of brackets
    where at least one bracket in the subsequence is nested.
    '''
    stack = []
    for char in string:
        if char == '[':
            stack.append(char)
        elif char == ']' and stack:
            stack.pop()
            if stack:
                return True
    return False
