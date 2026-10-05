import math

def poly(xs: list, x: float):
    return sum([coeff * math.pow(x, i) for i, coeff in enumerate(xs)])

def find_zero(xs: list):
    n = len(xs) - 1
    if n % 2 != 0:
        raise ValueError("xs must have even number of coefficients")
    if xs[-1] == 0:
        raise ValueError("largest coefficient must be non-zero")
    
    # Use Newton's method with a good initial guess
    # For a polynomial with even degree and positive leading coefficient,
    # a large positive x gives positive value, large negative x gives positive value
    # so there must be a root. Start with x = 1 and iterate.
    x = 1.0
    for _ in range(100):
        fx = poly(xs, x)
        if abs(fx) < 1e-12:
            return x
        # derivative
        dfx = sum([i * coeff * math.pow(x, i-1) for i, coeff in enumerate(xs) if i > 0])
        if dfx == 0:
            break
        x = x - fx / dfx
    return x
