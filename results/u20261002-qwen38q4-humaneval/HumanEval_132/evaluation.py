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
    """
    Create a function that takes a string as input which contains only square brackets.
    The function should return True if and only if there is a valid subsequence of brackets 
    where at least one bracket in the subsequence is nested.
    """
    # We need to check if there exists a valid subsequence of brackets where at least one bracket is nested.
    # A valid subsequence means we can pick some brackets from the string (in order) that form a valid bracket sequence.
    # A bracket is nested if it's inside another bracket pair.
    
    # One approach: check if there's a valid subsequence with depth >= 2.
    # We can use dynamic programming or greedy approach.
    
    # Let's think about it differently:
    # A valid bracket subsequence with nesting means we have at least one pair of brackets that contains another pair.
    # So we need to find indices i < j < k < l such that string[i] = '[', string[j] = '[', string[k] = ']', string[l] = ']'
    # and the subsequence string[i], string[j], string[k], string[l] forms a valid bracket sequence "[[]]".
    
    # Actually, we just need to check if there exists a valid subsequence with at least one nested bracket.
    # This is equivalent to checking if we can find a valid subsequence of length at least 4 that forms "[[]]".
    
    # Let's use a greedy/DP approach:
    # We track the maximum depth we can achieve in a valid subsequence.
    
    # Alternative approach: 
    # A valid subsequence with nesting exists if and only if we can find two pairs of brackets where one pair is inside the other.
    # This means we need to find indices i < j < k < l such that:
    # string[i] = '[', string[j] = '[', string[k] = ']', string[l] = ']'
    # and the subsequence formed by these four characters is valid.
    
    # Actually, let's think more carefully. We need a valid subsequence (not necessarily contiguous) where at least one bracket is nested.
    # The simplest such subsequence is "[[]]" which has length 4.
    
    # So we need to check if there exist indices i < j < k < l such that:
    # string[i] = '[', string[j] = '[', string[k] = ']', string[l] = ']'
    
    # Let's implement this check:
    n = len(string)
    if n < 4:
        return False
    
    # Find all positions of '[' and ']'
    # We need to find i < j < k < l where string[i] = '[', string[j] = '[', string[k] = ']', string[l] = ']'
    
    # We can do this efficiently:
    # For each potential j (second '['), we need:
    # - at least one '[' before j (for i)
    # - at least one ']' after j (for k)
    # - at least one ']' after k (for l)
    
    # Let's precompute:
    # left_count[i] = number of '[' in string[0:i]
    # right_count[i] = number of ']' in string[i:n]
    
    left_count = [0] * (n + 1)
    for i in range(n):
        left_count[i + 1] = left_count[i] + (1 if string[i] == '[' else 0)
    
    right_count = [0] * (n + 1)
    for i in range(n - 1, -1, -1):
        right_count[i] = right_count[i + 1] + (1 if string[i] == ']' else 0)
    
    # Now for each position j where string[j] == '[':
    # We need left_count[j] >= 1 (at least one '[' before j)
    # And we need to find k > j where string[k] == ']' and right_count[k + 1] >= 1 (at least one ']' after k)
    
    for j in range(n):
        if string[j] != '[':
            continue
        if left_count[j] < 1:
            continue
        # Now we need to find k > j where string[k] == ']' and right_count[k + 1] >= 1
        # We can iterate k from j+1 to n-1
        for k in range(j + 1, n):
            if string[k] == ']':
                if right_count[k + 1] >= 1:
                    return True
    
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
print('PASS_5c33c176c46f47b48790e925d532af1f')
