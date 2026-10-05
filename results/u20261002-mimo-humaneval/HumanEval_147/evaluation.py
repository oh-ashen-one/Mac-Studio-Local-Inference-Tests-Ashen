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


def get_max_triples(n):
    """
    You are given a positive integer n. You have to create an integer array a of length n.
        For each i (1 ≤ i ≤ n), the value of a[i] = i * i - i + 1.
        Return the number of triples (a[i], a[j], a[k]) of a where i < j < k, 
    and a[i] + a[j] + a[k] is a multiple of 3.

    Example :
        Input: n = 5
        Output: 1
        Explanation: 
        a = [1, 3, 7, 13, 21]
        The only valid triple is (1, 7, 13).
    """

def get_max_triples(n):
    """
    You are given a positive integer n. You have to create an integer array a of length n.
        For each i (1 ≤ i ≤ n), the value of a[i] = i * i - i + 1.
        Return the number of triples (a[i], a[j], a[k]) of a where i < j < k, 
    and a[i] + a[j] + a[k] is a multiple of 3.
    """
    # a[i] = i^2 - i + 1
    # We only care about a[i] % 3.
    # i^2 - i + 1 = i(i-1) + 1.
    # i(i-1) is the product of two consecutive integers, so it is always even.
    # Let's check i(i-1) % 3:
    # If i % 3 == 0, i(i-1) % 3 == 0.
    # If i % 3 == 1, i(i-1) % 3 == 1*0 == 0.
    # If i % 3 == 2, i(i-1) % 3 == 2*1 == 2.
    # So i(i-1) % 3 is 0 if i % 3 != 2, and 2 if i % 3 == 2.
    # Then a[i] % 3 = (i(i-1) + 1) % 3.
    # If i % 3 != 2, a[i] % 3 = (0 + 1) % 3 = 1.
    # If i % 3 == 2, a[i] % 3 = (2 + 1) % 3 = 0.
    
    # So a[i] % 3 is 1 if i % 3 is 0 or 1.
    # a[i] % 3 is 0 if i % 3 is 2.
    
    # We need to count triples (i, j, k) with i < j < k such that
    # (a[i] + a[j] + a[k]) % 3 == 0.
    
    # Let's count how many indices i (1 <= i <= n) have i % 3 == 0, 1, 2.
    # Let c0 = count of i where i % 3 == 0
    # Let c1 = count of i where i % 3 == 1
    # Let c2 = count of i where i % 3 == 2
    
    # For a[i] % 3:
    # If i % 3 == 0 -> a[i] % 3 == 1
    # If i % 3 == 1 -> a[i] % 3 == 1
    # If i % 3 == 2 -> a[i] % 3 == 0
    
    # So we have:
    # count of a[i] % 3 == 1 is c0 + c1
    # count of a[i] % 3 == 0 is c2
    # count of a[i] % 3 == 2 is 0
    
    # We need sum of three elements to be divisible by 3.
    # Possible combinations of remainders (r1, r2, r3) where r1+r2+r3 % 3 == 0:
    # (0, 0, 0)
    # (1, 1, 1)
    # (0, 1, 2) - but we have no elements with remainder 2.
    
    # So we only need to count:
    # 1. Triples where all three have remainder 0.
    # 2. Triples where all three have remainder 1.
    
    # Let n0 = c2 (count of remainder 0)
    # Let n1 = c0 + c1 (count of remainder 1)
    
    # Number of triples with all remainder 0: C(n0, 3)
    # Number of triples with all remainder 1: C(n1, 3)
    
    # Calculate c0, c1, c2 for i in 1..n
    c0 = n // 3
    c1 = (n + 2) // 3 - (n + 1) // 3
    # Actually simpler:
    # i = 1, 2, 3, ..., n
    # i % 3 == 1: 1, 4, 7, ... count = (n + 2) // 3
    # i % 3 == 2: 2, 5, 8, ... count = (n + 1) // 3
    # i % 3 == 0: 3, 6, 9, ... count = n // 3
    
    c1 = (n + 2) // 3
    c2 = (n + 1) // 3
    c0 = n // 3
    
    n0 = c2
    n1 = c0 + c1
    
    def comb3(x):
        if x < 3:
            return 0
        return x * (x - 1) * (x - 2) // 6
    
    return comb3(n0) + comb3(n1)

def check(candidate):

    assert candidate(5) == 1
    assert candidate(6) == 4
    assert candidate(10) == 36
    assert candidate(100) == 53361

check(get_max_triples)
print('PASS_e19eb5c4d12f4491bacbb594f9fb5fc7')
