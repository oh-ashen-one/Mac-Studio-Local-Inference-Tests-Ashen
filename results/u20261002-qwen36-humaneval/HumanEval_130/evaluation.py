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


def tri(n):
    """Everyone knows Fibonacci sequence, it was studied deeply by mathematicians in 
    the last couple centuries. However, what people don't know is Tribonacci sequence.
    Tribonacci sequence is defined by the recurrence:
    tri(1) = 3
    tri(n) = 1 + n / 2, if n is even.
    tri(n) =  tri(n - 1) + tri(n - 2) + tri(n + 1), if n is odd.
    For example:
    tri(2) = 1 + (2 / 2) = 2
    tri(4) = 3
    tri(3) = tri(2) + tri(1) + tri(4)
           = 2 + 3 + 3 = 8 
    You are given a non-negative integer number n, you have to a return a list of the 
    first n + 1 numbers of the Tribonacci sequence.
    Examples:
    tri(3) = [1, 3, 2, 8]
    """

def tri(n):
    """
    Compute the first n+1 numbers of the Tribonacci sequence as defined by:
    tri(1) = 3
    tri(n) = 1 + n / 2, if n is even.
    tri(n) = tri(n - 1) + tri(n - 2) + tri(n + 1), if n is odd.
    
    Returns a list of the first n+1 numbers (indices 0 to n).
    
    Note: The problem states tri(1) = 3, but the example shows tri(3) = [1, 3, 2, 8].
    This suggests that the sequence is 0-indexed in the output, where:
    - tri(0) = 1 (implied, since the first element is 1)
    - tri(1) = 3
    - tri(2) = 2
    - tri(3) = 8
    
    Let's re-read the specification carefully:
    - tri(1) = 3
    - tri(n) = 1 + n / 2, if n is even.
    - tri(n) = tri(n - 1) + tri(n - 2) + tri(n + 1), if n is odd.
    
    The example says tri(3) = [1, 3, 2, 8], which is a list of 4 elements (n+1 = 4 when n=3).
    So the list contains tri(0), tri(1), tri(2), tri(3).
    
    We need to figure out tri(0). The example shows the first element is 1, so tri(0) = 1.
    
    Let's verify:
    - tri(0) = 1 (base case, implied)
    - tri(1) = 3 (given)
    - tri(2): n=2 is even, so tri(2) = 1 + 2/2 = 1 + 1 = 2. ✓
    - tri(3): n=3 is odd, so tri(3) = tri(2) + tri(1) + tri(4).
      We need tri(4). n=4 is even, so tri(4) = 1 + 4/2 = 1 + 2 = 3.
      So tri(3) = 2 + 3 + 3 = 8. ✓
    
    So the sequence is:
    tri(0) = 1
    tri(1) = 3
    tri(2) = 2
    tri(3) = 8
    tri(4) = 3
    ...
    
    The challenge is that for odd n, tri(n) depends on tri(n+1), which creates a circular dependency.
    We need to solve this carefully.
    
    For even n: tri(n) = 1 + n // 2 (using integer division since the result should be integer)
    For odd n: tri(n) = tri(n-1) + tri(n-2) + tri(n+1)
    
    But tri(n+1) for odd n is tri of an even number, which we can compute directly.
    
    So for odd n:
    tri(n) = tri(n-1) + tri(n-2) + (1 + (n+1) // 2)
    
    Wait, let's check: n=3 (odd), tri(3) = tri(2) + tri(1) + tri(4)
    tri(4) = 1 + 4//2 = 3
    tri(3) = 2 + 3 + 3 = 8. ✓
    
    So we can compute iteratively:
    - tri(0) = 1
    - tri(1) = 3
    - For n >= 2:
      - If n is even: tri(n) = 1 + n // 2
      - If n is odd: tri(n) = tri(n-1) + tri(n-2) + (1 + (n+1) // 2)
    
    Let's verify tri(5):
    n=5 is odd.
    tri(5) = tri(4) + tri(3) + tri(6)
    tri(6) = 1 + 6//2 = 1 + 3 = 4
    tri(5) = 3 + 8 + 4 = 15
    
    Let's verify tri(6):
    n=6 is even.
    tri(6) = 1 + 6//2 = 4. ✓
    
    So the algorithm is:
    1. Start with a list containing [1, 3] for n >= 1.
    2. For each i from 2 to n:
       - If i is even: append 1 + i // 2
       - If i is odd: append tri(i-1) + tri(i-2) + (1 + (i+1) // 2)
    
    Return the list of length n+1.
    """
    if n == 0:
        return [1]
    
    # Initialize with tri(0) and tri(1)
    result = [1, 3]
    
    for i in range(2, n + 1):
        if i % 2 == 0:
            # Even case
            val = 1 + i // 2
            result.append(val)
        else:
            # Odd case: tri(i) = tri(i-1) + tri(i-2) + tri(i+1)
            # tri(i+1) is even, so tri(i+1) = 1 + (i+1) // 2
            tri_i_plus_1 = 1 + (i + 1) // 2
            val = result[i - 1] + result[i - 2] + tri_i_plus_1
            result.append(val)
    
    return result

def check(candidate):

    # Check some simple cases
    
    assert candidate(3) == [1, 3, 2.0, 8.0]
    assert candidate(4) == [1, 3, 2.0, 8.0, 3.0]
    assert candidate(5) == [1, 3, 2.0, 8.0, 3.0, 15.0]
    assert candidate(6) == [1, 3, 2.0, 8.0, 3.0, 15.0, 4.0]
    assert candidate(7) == [1, 3, 2.0, 8.0, 3.0, 15.0, 4.0, 24.0]
    assert candidate(8) == [1, 3, 2.0, 8.0, 3.0, 15.0, 4.0, 24.0, 5.0]
    assert candidate(9) == [1, 3, 2.0, 8.0, 3.0, 15.0, 4.0, 24.0, 5.0, 35.0]
    assert candidate(20) == [1, 3, 2.0, 8.0, 3.0, 15.0, 4.0, 24.0, 5.0, 35.0, 6.0, 48.0, 7.0, 63.0, 8.0, 80.0, 9.0, 99.0, 10.0, 120.0, 11.0]

    # Check some edge cases that are easy to work out by hand.
    assert candidate(0) == [1]
    assert candidate(1) == [1, 3]

check(tri)
print('PASS_1cd227f7deda40d88bcd83aa4f022967')
