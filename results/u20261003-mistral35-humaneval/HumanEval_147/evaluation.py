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

from collections import defaultdict

def get_max_triples(n):
    a = [i * i - i + 1 for i in range(1, n + 1)]
    mod_counts = defaultdict(int)
    for num in a:
        mod_counts[num % 3] += 1

    count = 0
    # Case 1: All three numbers are divisible by 3 (0 mod 3)
    count += mod_counts[0] * (mod_counts[0] - 1) * (mod_counts[0] - 2) // 6
    # Case 2: All three numbers are 1 mod 3
    count += mod_counts[1] * (mod_counts[1] - 1) * (mod_counts[1] - 2) // 6
    # Case 3: All three numbers are 2 mod 3
    count += mod_counts[2] * (mod_counts[2] - 1) * (mod_counts[2] - 2) // 6
    # Case 4: One from each mod (0, 1, 2)
    count += mod_counts[0] * mod_counts[1] * mod_counts[2]

    return count

def check(candidate):

    assert candidate(5) == 1
    assert candidate(6) == 4
    assert candidate(10) == 36
    assert candidate(100) == 53361

check(get_max_triples)
print('PASS_1b31bba8fd0a43a0978d0ee9c4115262')
