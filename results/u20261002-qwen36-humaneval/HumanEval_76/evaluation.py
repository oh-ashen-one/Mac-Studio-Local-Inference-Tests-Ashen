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


def is_simple_power(x, n):
    """Your task is to write a function that returns true if a number x is a simple
    power of n and false in other cases.
    x is a simple power of n if n**int=x
    For example:
    is_simple_power(1, 4) => true
    is_simple_power(2, 2) => true
    is_simple_power(8, 2) => true
    is_simple_power(3, 2) => false
    is_simple_power(3, 1) => false
    is_simple_power(5, 3) => false
    """

def is_simple_power(x, n):
    """
    Returns true if x is a simple power of n, i.e., x = n**k for some non-negative integer k.
    
    Examples:
    is_simple_power(1, 4) => True (4**0 = 1)
    is_simple_power(2, 2) => True (2**1 = 2)
    is_simple_power(8, 2) => True (2**3 = 8)
    is_simple_power(3, 2) => False
    is_simple_power(3, 1) => False
    is_simple_power(5, 3) => False
    """
    # Handle edge cases
    if n == 0:
        # 0**k is 0 for k >= 1, 0**0 is 1
        if x == 1:
            return True
        if x == 0:
            return True  # 0**1 = 0, but let's think... 0**k for k>=1 is 0
            # Actually 0**0 = 1, 0**1 = 0, 0**2 = 0, etc.
            # So x=0 is a power of 0 (0**1 = 0)
        return False
    
    if n == 1:
        # 1**k = 1 for all k >= 0
        return x == 1
    
    if n == -1:
        # (-1)**k is 1 if k is even, -1 if k is odd
        return x == 1 or x == -1
    
    if x == 1:
        # n**0 = 1 for any n != 0
        return True
    
    if x == 0:
        # n**k = 0 only if n = 0 and k >= 1, but we handled n=0 above
        return False
    
    # For |n| >= 2, we need to check if x = n**k for some integer k >= 1
    # We can do this by repeatedly dividing x by n
    
    # Handle negative n
    if n < 0:
        # n is negative, so n**k alternates sign
        # x must have the same sign pattern
        # Let's work with absolute values
        abs_n = abs(n)
        abs_x = abs(x)
        
        # Check if abs_x is a power of abs_n
        while abs_x > 1:
            if abs_x % abs_n != 0:
                return False
            abs_x //= abs_n
        
        # Now abs_x should be 1
        if abs_x != 1:
            return False
        
        # Now check the sign: n**k should equal x
        # n is negative, so n**k is positive if k is even, negative if k is odd
        # We need to find k such that abs_n**k = abs_x (which is 1, so k=0)
        # But k=0 gives n**0 = 1, not x (unless x=1)
        # Wait, let me reconsider.
        
        # If x = n**k for some integer k >= 1:
        # abs(x) = abs(n)**k
        # sign(x) = sign(n)**k
        
        # We already verified abs(x) = abs(n)**k for some k
        # Now we need to check if sign(x) matches sign(n)**k
        
        # Let's find k from the absolute value check
        # We divided abs_x by abs_n repeatedly until it became 1
        # The number of divisions is k
        
        # Actually, let me redo this more carefully
        pass
    
    # Let's use a cleaner approach for all cases
    if n == 0:
        return x == 0 or x == 1  # 0**0=1, 0**k=0 for k>=1
    
    if n == 1:
        return x == 1
    
    if n == -1:
        return x == 1 or x == -1
    
    # For |n| >= 2
    abs_n = abs(n)
    abs_x = abs(x)
    
    # Check if abs_x is a power of abs_n
    k = 0
    val = 1
    while val < abs_x:
        val *= abs_n
        k += 1
    
    if val != abs_x:
        return False
    
    # Now val = abs_n**k = abs_x
    # Check if n**k = x
    # n**k has sign: if n > 0, sign is positive; if n < 0, sign is (-1)**k
    if n > 0:
        return x == val
    else:
        # n is negative
        if k % 2 == 0:
            return x == val  # (-n)**even = positive
        else:
            return x == -val  # (-n)**odd = negative

def check(candidate):

    # Check some simple cases
    assert candidate(16, 2)== True, "This prints if this assert fails 1 (good for debugging!)"
    assert candidate(143214, 16)== False, "This prints if this assert fails 1 (good for debugging!)"
    assert candidate(4, 2)==True, "This prints if this assert fails 1 (good for debugging!)"
    assert candidate(9, 3)==True, "This prints if this assert fails 1 (good for debugging!)"
    assert candidate(16, 4)==True, "This prints if this assert fails 1 (good for debugging!)"
    assert candidate(24, 2)==False, "This prints if this assert fails 1 (good for debugging!)"
    assert candidate(128, 4)==False, "This prints if this assert fails 1 (good for debugging!)"
    assert candidate(12, 6)==False, "This prints if this assert fails 1 (good for debugging!)"

    # Check some edge cases that are easy to work out by hand.
    assert candidate(1, 1)==True, "This prints if this assert fails 2 (also good for debugging!)"
    assert candidate(1, 12)==True, "This prints if this assert fails 2 (also good for debugging!)"


check(is_simple_power)
print('PASS_ac54eabd85f144a1a7e10d975c22ed55')
