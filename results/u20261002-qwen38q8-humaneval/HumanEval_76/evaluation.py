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
    if n == 1:
        return x == 1
    if n == 0:
        return x == 1  # 0**0 is 1, but 0**positive is 0, so only x==1 works for n=0? Actually 0**0=1, 0**1=0, etc. Let's think: if n=0, then n**k for k>=1 is 0, and 0**0=1. So x can be 1 (k=0) or 0 (k>=1). But the problem says "simple power" meaning n**int = x. For n=0, x=1 (0**0) or x=0 (0**1, 0**2, ...). Hmm, but let's check the examples. The examples don't include n=0. Let's handle it carefully.
        # Actually, let's reconsider. The problem likely assumes n >= 1. But to be safe, let's handle edge cases.
        # For n=0: 0**0 = 1, 0**k = 0 for k >= 1. So x can be 1 or 0.
        # But wait, is 0**0 considered? In Python, 0**0 is 1. Let's include both.
        return x == 1 or x == 0
    if n < 0:
        # Negative base: n**k can be positive or negative depending on k.
        # This is more complex. Let's handle it by checking if x is a power of n.
        # For negative n, n**k = x. If k is even, x is positive; if k is odd, x is negative.
        # We can check by taking absolute values and then checking sign.
        if x == 0:
            return False  # n**k is never 0 for n != 0
        # Check if |x| is a power of |n|
        abs_n = abs(n)
        abs_x = abs(x)
        if abs_x == 1:
            # 1 can be n**0 for any n, or (-1)**even for n=-1
            return True
        # Check if abs_x is a power of abs_n
        power = 1
        k = 0
        while power < abs_x:
            power *= abs_n
            k += 1
            if power > abs_x:
                break
        if power != abs_x:
            return False
        # Now check the sign
        if n < 0:
            # n**k has sign (-1)**k
            if k % 2 == 0:
                return x > 0
            else:
                return x < 0
        else:
            return x > 0
    # n >= 2
    if x == 1:
        return True  # n**0 = 1
    if x < 1:
        return False
    power = 1
    while power < x:
        power *= n
    return power == x

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
print('PASS_c58b7c154ea74d509f3ef7f42668a298')
