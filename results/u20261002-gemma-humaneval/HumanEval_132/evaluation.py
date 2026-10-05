import ast as _bench_ast
import operator as _bench_operator
def _bench_arithmetic_node(n):
    if isinstance(n, _bench_ast.Constant) and type(n.value) in (int, float): return n.value
    if isinstance(n, _bench_ast.UnaryOp) and isinstance(n.op, (_bench_ast.UAdd, _bench_ast.USub)):
        v = _bench_arithmetic_node(n.operand)
        return v if isinstance(n.op, _bench_ast.UAdd) else -v
    ops = {_bench_ast.Add: _bench_operator.add, _bench_ast.Sub: _bench_operator.sub, _bench_ast.Mult: _bench_operator.mul, _bench_ast.Div: _bench_operator.truediv, _bench_ast.FloorDiv: _bench_operator.floordiv, _bench_ast.Mod: _bench_operator.mod, _bench_ast.Pow: _bench_operator.pow}
    if isinstance(n, _bench_ast.BinOp) and type(n.op) in ops:
        return ops[type(n.op)](_bench_arithmetic_node(n.left), _bench_arithmetic_node(n.right))
    raise ValueError('Only numeric arithmetic is permitted by benchmark eval')
def eval(expression):
    return _bench_arithmetic_node(_bench_ast.parse(expression, mode='eval').body)


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

def check(candidate):

    # Check some simple cases
    assert candidate('[[]]') == True, "This prints if this assert fails 1 (good for debugging!)"
    assert candidate('[]]]]]]][[[[[]') == False
    assert candidate('[][]') == False
    assert candidate(('[]')) == False
    assert candidate('[[[[]]]]') == True
    assert candidate('[]]]]]]]]]]') == False
    assert candidate('[][][[]]') == True
    assert candidate('[[]') == False
    assert candidate('[]]') == False
    assert candidate('[[]][[') == True
    assert candidate('[[][]]') == True

    # Check some edge cases that are easy to work out by hand.
    assert candidate('') == False, "This prints if this assert fails 2 (also good for debugging!)"
    assert candidate('[[[[[[[[') == False
    assert candidate(']]]]]]]]') == False


check(is_nested)
print('PASS_5c111470c37341f2ba657aed27fb9d27')
