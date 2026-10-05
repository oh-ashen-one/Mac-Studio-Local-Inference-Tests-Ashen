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
    # We need to count triples (i, j, k) with i < j < k such that (a[i] + a[j] + a[k]) % 3 == 0
    
    # First, let's figure out the pattern of a[i] mod 3
    # a[i] = i^2 - i + 1
    # Let's compute for i mod 3:
    # i mod 3 = 0: i^2 mod 3 = 0, i mod 3 = 0, so a[i] mod 3 = 0 - 0 + 1 = 1
    # i mod 3 = 1: i^2 mod 3 = 1, i mod 3 = 1, so a[i] mod 3 = 1 - 1 + 1 = 1
    # i mod 3 = 2: i^2 mod 3 = 4 mod 3 = 1, i mod 3 = 2, so a[i] mod 3 = 1 - 2 + 1 = 0
    
    # So:
    # If i % 3 == 0: a[i] % 3 = 1
    # If i % 3 == 1: a[i] % 3 = 1
    # If i % 3 == 2: a[i] % 3 = 0
    
    # Let's verify with the example:
    # i=1: a[1] = 1*1 - 1 + 1 = 1, 1 % 3 = 1. i%3=1, matches.
    # i=2: a[2] = 4 - 2 + 1 = 3, 3 % 3 = 0. i%3=2, matches.
    # i=3: a[3] = 9 - 3 + 1 = 7, 7 % 3 = 1. i%3=0, matches.
    # i=4: a[4] = 16 - 4 + 1 = 13, 13 % 3 = 1. i%3=1, matches.
    # i=5: a[5] = 25 - 5 + 1 = 21, 21 % 3 = 0. i%3=2, matches.
    
    # So the residues are:
    # i=1: 1
    # i=2: 0
    # i=3: 1
    # i=4: 1
    # i=5: 0
    # i=6: 1
    # i=7: 0
    # i=8: 1
    # i=9: 1
    # i=10: 0
    
    # Pattern of residues (starting from i=1): 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, ...
    # Let's group by i mod 3:
    # i mod 3 = 1: residue 1
    # i mod 3 = 2: residue 0
    # i mod 3 = 0: residue 1
    
    # So for each i:
    # if i % 3 == 1: residue = 1
    # if i % 3 == 2: residue = 0
    # if i % 3 == 0: residue = 1
    
    # Now we need to count triples (i, j, k) with i < j < k such that (res[i] + res[j] + res[k]) % 3 == 0
    
    # Let's count how many indices have each residue:
    # count[0] = number of i in [1, n] with residue 0
    # count[1] = number of i in [1, n] with residue 1
    # count[2] = number of i in [1, n] with residue 2 (should be 0 based on our analysis)
    
    # From our analysis:
    # residue 0 occurs when i % 3 == 2
    # residue 1 occurs when i % 3 == 0 or i % 3 == 1
    # residue 2 never occurs
    
    # So:
    # count[0] = number of i in [1, n] with i % 3 == 2
    # count[1] = number of i in [1, n] with i % 3 == 0 or i % 3 == 1
    # count[2] = 0
    
    # Let's compute these counts:
    # For i in [1, n]:
    # i % 3 == 0: i = 3, 6, 9, ... -> floor(n/3)
    # i % 3 == 1: i = 1, 4, 7, ... -> floor((n-1)/3) + 1 if n >= 1, which is (n+2)//3
    # i % 3 == 2: i = 2, 5, 8, ... -> floor((n-2)/3) + 1 if n >= 2, which is (n+1)//3
    
    # Let me verify:
    # n=5:
    # i%3==0: i=3 -> 1 = floor(5/3) = 1
    # i%3==1: i=1,4 -> 2 = (5+2)//3 = 7//3 = 2
    # i%3==2: i=2,5 -> 2 = (5+1)//3 = 6//3 = 2
    
    # So:
    # count[0] = (n+1)//3
    # count[1] = floor(n/3) + (n+2)//3
    # count[2] = 0
    
    # Now, we need to count triples (i, j, k) with i < j < k such that (res[i] + res[j] + res[k]) % 3 == 0
    
    # Since residue 2 never occurs, the possible sums mod 3 are:
    # 0+0+0 = 0
    # 0+0+1 = 1
    # 0+1+1 = 2
    # 1+1+1 = 3 = 0
    
    # So valid triples are:
    # 1. All three have residue 0: C(count[0], 3)
    # 2. All three have residue 1: C(count[1], 3)
    
    # Wait, let me double-check. The sum must be 0 mod 3.
    # Possible combinations of residues (each is 0 or 1):
    # (0,0,0): sum = 0, valid
    # (0,0,1): sum = 1, invalid
    # (0,1,1): sum = 2, invalid
    # (1,1,1): sum = 3 = 0, valid
    
    # So yes, only (0,0,0) and (1,1,1) are valid.
    
    def comb3(m):
        """Return C(m, 3) = m*(m-1)*(m-2)/6 if m >= 3, else 0."""
        if m < 3:
            return 0
        return m * (m - 1) * (m - 2) // 6
    
    count0 = (n + 1) // 3
    count1 = n // 3 + (n + 2) // 3
    
    result = comb3(count0) + comb3(count1)
    
    return result

def check(candidate):

    assert candidate(5) == 1
    assert candidate(6) == 4
    assert candidate(10) == 36
    assert candidate(100) == 53361

check(get_max_triples)
print('PASS_b3c694f95b7e4adea48fd3d3f5e6a685')
