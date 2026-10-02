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

    is_nested('[[]]') ➞ True
    is_nested('[]]]]]]][[[[[]') ➞ False
    is_nested('[][]') ➞ False
    is_nested('[]') ➞ False
    is_nested('[[][]]') ➞ True
    is_nested('[[]][[') ➞ True
    '''
    # A nested bracket means there exists a pair of brackets that contains another pair.
    # For example, '[[]]' has a nested structure: the outer [] contains another [].
    # '[[][]]' also has nesting: the outer [] contains two inner pairs, and one of them is nested within the outer.
    # '[[]][[' has a nested part: the first '[[]]' is nested.
    
    # We need to find if there exists a valid subsequence of brackets that is properly balanced
    # AND has at least one level of nesting (i.e., depth >= 2 at some point).
    
    # Actually, let's think about what "valid subsequence" means.
    # A subsequence is obtained by deleting zero or more characters from the original string.
    # A valid subsequence of brackets means it's a properly balanced bracket sequence.
    # "at least one bracket in the subsequence is nested" means the subsequence has nesting,
    # i.e., it's not just a sequence of independent pairs like "[][]" but has something like "[[]]".
    
    # So we need to check: does there exist a subsequence of the string that is a valid (balanced) bracket sequence
    # with depth >= 2?
    
    # Let's think differently. If we can find any occurrence of "[[]]" as a subsequence, then we have nesting.
    # More precisely, if there exist indices i < j < k < l such that string[i] == '[', string[j] == '[', 
    # string[k] == ']', string[l] == ']', and i < j < k < l, then we have a nested pair "[[]]" as a subsequence.
    # This would give us a valid subsequence "[[]]" which is nested.
    
    # But wait, is that sufficient? Let's check the examples:
    # '[[]]' -> True: we have indices 0,1,2,3 forming "[[]]" -> nested.
    # '[]]]]]]][[[[[]' -> False: Let's see. We have '[]' at the start, then many ']', then '[[[[]'. 
    #   Can we form a nested subsequence? We need i < j < k < l with '[', '[', ']', ']'.
    #   The string is: '[]]]]]]][[[[[]'
    #   Indices: 0:'[', 1:']', 2:']', 3:']', 4:']', 5:']', 6:']', 7:'[', 8:'[', 9:'[', 10:'[', 11:'[', 12:']'
    #   We need two '[' and two ']' with the first '[' before the second '[' before the first ']' before the second ']'.
    #   Let's try: i=0 ('['), j=7 ('['), k=1 (']'), l=12 (']'). But j=7 > k=1, so i < j < k < l doesn't hold.
    #   We need i < j < k < l. So we need two '[' that come before two ']' where the second '[' comes before the first ']'.
    #   In this string, all ']' before index 7 are at indices 1-6, and all '[' after index 7 are at 7-11, with one ']' at 12.
    #   So we can pick i=0, j=7, k=12, l=... we need another ']'. There's no other ']' after index 12.
    #   Can we pick i=0, j=8, k=12, l=... no second ']' after 12.
    #   What about using ']' from before? i=0, j=7, k=1, l=12: but 7 > 1, so not i < j < k < l.
    #   So no nested subsequence exists. Returns False. Correct.
    
    # '[][]' -> False: We have '[', ']', '[', ']'. Can we form "[[]]" as subsequence?
    #   We need i < j < k < l with '[', '[', ']', ']'.
    #   i=0 ('['), j=2 ('['), k=1 (']'), l=3 (']'). But j=2 > k=1, so no.
    #   i=0, j=2, k=3, l=... no second ']' after 3.
    #   So no nested subsequence. Returns False. Correct.
    
    # '[]' -> False: Only one pair, no nesting. Correct.
    
    # '[[][]]' -> True: We have '[', '[', ']', '[', ']', ']'.
    #   Can we find i < j < k < l? i=0, j=1, k=2, l=5: string[0]='[', string[1]='[', string[2]=']', string[5]=']'. Yes!
    #   So returns True. Correct.
    
    # '[[]][[' -> True: We have '[', '[', ']', ']', '[', '['.
    #   i=0, j=1, k=2, l=3: string[0]='[', string[1]='[', string[2]=']', string[3]=']'. Yes!
    #   So returns True. Correct.
    
    # So the problem reduces to: does there exist indices i < j < k < l such that
    # string[i] == '[', string[j] == '[', string[k] == ']', string[l] == ']'?
    
    # This is equivalent to: can we find two '[' and two ']' such that the second '[' comes before the first ']'?
    # In other words, is there a point where we've seen at least 2 '[' and at least 2 ']' with the constraint that
    # the second '[' appears before the first ']' among the chosen ones?
    
    # A simpler way: iterate through the string and keep track of the count of '[' and ']'.
    # We need to find if there exist i < j < k < l with the pattern "[[ ] ]".
    
    # Let's just check: for every pair of indices (j, k) where j < k, string[j] == '[' and string[k] == ']',
    # check if there exists i < j with string[i] == '[' and l > k with string[l] == ']'.
    
    # A more efficient approach:
    # Find the first occurrence of '[', then find the second occurrence of '[' after that,
    # then find the first occurrence of ']' after the second '[', then find another ']' after that.
    
    # Let's implement this:
    n = len(string)
    
    # Find the first '['
    first_open = -1
    for i in range(n):
        if string[i] == '[':
            first_open = i
            break
    
    if first_open == -1:
        return False
    
    # Find the second '[' after first_open
    second_open = -1
    for j in range(first_open + 1, n):
        if string[j] == '[':
            second_open = j
            break
    
    if second_open == -1:
        return False
    
    # Find the first ']' after second_open
    first_close = -1
    for k in range(second_open + 1, n):
        if string[k] == ']':
            first_close = k
            break
    
    if first_close == -1:
        return False
    
    # Find another ']' after first_close
    for l in range(first_close + 1, n):
        if string[l] == ']':
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
print('PASS_304346b1e3bd4a33a69a7b9ba9edc3af')
