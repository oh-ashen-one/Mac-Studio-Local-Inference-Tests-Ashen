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

import math


def poly(xs: list, x: float):
    """
    Evaluates polynomial with coefficients xs at point x.
    return xs[0] + xs[1] * x + xs[1] * x^2 + .... xs[n] * x^n
    """
    return sum([coeff * math.pow(x, i) for i, coeff in enumerate(xs)])


def find_zero(xs: list):
    """ xs are coefficients of a polynomial.
    find_zero find x such that poly(x) = 0.
    find_zero returns only only zero point, even if there are many.
    Moreover, find_zero only takes list xs having even number of coefficients
    and largest non zero coefficient as it guarantees
    a solution.
    >>> round(find_zero([1, 2]), 2) # f(x) = 1 + 2x
    -0.5
    >>> round(find_zero([-6, 11, -6, 1]), 2) # (x - 1) * (x - 2) * (x - 3) = -6 + 11x - 6x^2 + x^3
    1.0
    """

import math


def poly(xs: list, x: float):
    """
    Evaluates polynomial with coefficients xs at point x.
    return xs[0] + xs[1] * x + xs[1] * x^2 + .... xs[n] * x^n
    """
    return sum([coeff * math.pow(x, i) for i, coeff in enumerate(xs)])


def find_zero(xs: list):
    """ xs are coefficients of a polynomial.
    find_zero find x such that poly(x) = 0.
    find_zero returns only only zero point, even if there are many.
    Moreover, find_zero only takes list xs having even number of coefficients
    and largest non zero coefficient as it guarantees
    a solution.
    >>> round(find_zero([1, 2]), 2) # f(x) = 1 + 2x
    -0.5
    >>> round(find_zero([-6, 11, -6, 1]), 2) # (x - 1) * (x - 2) * (x - 3) = -6 + 11x - 6x^2 + x^3
    1.0
    """
    # Use bisection method to find a zero
    # First, find a bracket [a, b] where poly(a) and poly(b) have opposite signs
    
    # Try a range of values to find a sign change
    # Start with a reasonable range
    a = -1000.0
    b = 1000.0
    
    # Check if we already have a zero at endpoints
    fa = poly(xs, a)
    fb = poly(xs, b)
    
    # If no sign change in the initial range, try expanding or use a different approach
    # For polynomials with even number of coefficients (odd degree), there's always at least one real root
    # Let's try to find a bracket by scanning
    
    # Try smaller ranges first
    found_bracket = False
    for scale in [1, 10, 100, 1000, 10000]:
        a = -scale
        b = scale
        fa = poly(xs, a)
        fb = poly(xs, b)
        if fa * fb <= 0:
            found_bracket = True
            break
    
    if not found_bracket:
        # Try scanning for sign changes
        step = 1.0
        prev_x = -1000.0
        prev_f = poly(xs, prev_x)
        for i in range(2000):
            curr_x = -1000.0 + i * step
            curr_f = poly(xs, curr_x)
            if prev_f * curr_f <= 0:
                a = prev_x
                b = curr_x
                found_bracket = True
                break
            prev_x = curr_x
            prev_f = curr_f
    
    if not found_bracket:
        # As a fallback, try a very wide range
        a = -1e6
        b = 1e6
        fa = poly(xs, a)
        fb = poly(xs, b)
        if fa * fb > 0:
            # This shouldn't happen for odd-degree polynomials, but handle it
            # Try to find any sign change
            for i in range(1000):
                x1 = -1e6 + i * 2000
                x2 = x1 + 2000
                f1 = poly(xs, x1)
                f2 = poly(xs, x2)
                if f1 * f2 <= 0:
                    a = x1
                    b = x2
                    break
    
    # Now use bisection to find the zero
    fa = poly(xs, a)
    fb = poly(xs, b)
    
    # If one endpoint is already a zero, return it
    if abs(fa) < 1e-10:
        return a
    if abs(fb) < 1e-10:
        return b
    
    # Bisection method
    for _ in range(100):
        mid = (a + b) / 2
        fm = poly(xs, mid)
        if abs(fm) < 1e-10:
            return mid
        if fa * fm <= 0:
            b = mid
            fb = fm
        else:
            a = mid
            fa = fm
    
    return (a + b) / 2



METADATA = {}


def check(candidate):
    import math
    import random
    rng = random.Random(42)
    import copy
    for _ in range(100):
        ncoeff = 2 * rng.randint(1, 4)
        coeffs = []
        for _ in range(ncoeff):
            coeff = rng.randint(-10, 10)
            if coeff == 0:
                coeff = 1
            coeffs.append(coeff)
        solution = candidate(copy.deepcopy(coeffs))
        assert math.fabs(poly(coeffs, solution)) < 1e-4


check(find_zero)
print('PASS_60e83034a5414982848d8676109051b6')
