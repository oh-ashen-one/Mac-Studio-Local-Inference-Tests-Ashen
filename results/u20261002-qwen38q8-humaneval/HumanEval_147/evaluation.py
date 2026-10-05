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

    Example :
        Input: n = 5
        Output: 1
        Explanation: 
        a = [1, 3, 7, 13, 21]
        The only valid triple is (1, 7, 13).
    """
    # Compute a[i] mod 3 for i from 1 to n
    # a[i] = i*i - i + 1
    # Let's find the pattern of a[i] mod 3
    
    # i mod 3: 0, 1, 2
    # i=1: 1-1+1=1, mod 3 = 1
    # i=2: 4-2+1=3, mod 3 = 0
    # i=3: 9-3+1=7, mod 3 = 1
    # i=4: 16-4+1=13, mod 3 = 1
    # i=5: 25-5+1=21, mod 3 = 0
    # i=6: 36-6+1=31, mod 3 = 1
    # i=7: 49-7+1=43, mod 3 = 1
    # i=8: 64-8+1=57, mod 3 = 0
    # i=9: 81-9+1=73, mod 3 = 1
    
    # Pattern: for i mod 3:
    # i ≡ 0 (mod 3): i*i - i + 1 ≡ 0 - 0 + 1 = 1 (mod 3)
    # i ≡ 1 (mod 3): i*i - i + 1 ≡ 1 - 1 + 1 = 1 (mod 3)
    # i ≡ 2 (mod 3): i*i - i + 1 ≡ 4 - 2 + 1 = 3 ≡ 0 (mod 3)
    
    # So:
    # If i mod 3 == 0: a[i] mod 3 = 1
    # If i mod 3 == 1: a[i] mod 3 = 1
    # If i mod 3 == 2: a[i] mod 3 = 0
    
    # Count how many indices have each residue
    count_0 = 0  # a[i] mod 3 == 0
    count_1 = 0  # a[i] mod 3 == 1
    count_2 = 0  # a[i] mod 3 == 2
    
    for i in range(1, n + 1):
        r = i % 3
        if r == 0:
            count_1 += 1
        elif r == 1:
            count_1 += 1
        else:  # r == 2
            count_0 += 1
    
    # We need triples (i, j, k) with i < j < k such that a[i] + a[j] + a[k] ≡ 0 (mod 3)
    # The possible combinations of residues that sum to 0 mod 3:
    # (0, 0, 0): sum = 0
    # (1, 1, 1): sum = 3 ≡ 0
    # (0, 1, 2): sum = 3 ≡ 0
    # (0, 2, 1): same as above
    # (1, 0, 2): same as above
    # (1, 2, 0): same as above
    # (2, 0, 1): same as above
    # (2, 1, 0): same as above
    
    # But we only have residues 0 and 1 in our array (no residue 2)
    # So the valid combinations are:
    # (0, 0, 0): all three have residue 0
    # (1, 1, 1): all three have residue 1
    
    # Number of ways to choose 3 from count_0: C(count_0, 3)
    # Number of ways to choose 3 from count_1: C(count_1, 3)
    
    def comb3(x):
        if x < 3:
            return 0
        return x * (x - 1) * (x - 2) // 6
    
    return comb3(count_0) + comb3(count_1)

def check(candidate):

    assert candidate(5) == 1
    assert candidate(6) == 4
    assert candidate(10) == 36
    assert candidate(100) == 53361

check(get_max_triples)
print('PASS_2a2c60168dd543b8a938c604fd2aaa07')
