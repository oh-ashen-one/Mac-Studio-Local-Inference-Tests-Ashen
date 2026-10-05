def is_nested(string):
    '''
    Create a function that takes a string as input which contains only square brackets.
    The function should return True if and only if there is a valid subsequence of brackets 
    where at least one bracket in the subsequence is nested.

    is_nested('[[]]') ➞ True
    is_nested('[]]]]]]][[[[[]') ➞ False
    is_nested('[][]') ➞ False
    is_nested('[]') ➞ False
    is_nested('[[][]]') ➞ True
    is_nested('[[]][[') ➞ True
    '''
    stack = []
    for char in string:
        if char == '[':
            stack.append(char)
        elif char == ']':
            if stack:
                stack.pop()
                # If we just closed a bracket and the stack is not empty,
                # it means the bracket we just closed was nested inside another.
                if stack:
                    return True
    return False
