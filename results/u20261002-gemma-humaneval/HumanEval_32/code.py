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
    """
    # Bisection method
    # Since the polynomial has an odd degree (even number of coefficients),
    # it must have at least one real root.
    # We need to find an interval [a, b] where poly(a) and poly(b) have opposite signs.
    
    def f(x):
        return poly(xs, x)

    # Search for a range [a, b] that brackets the root
    a = -1.0
    b = 1.0
    while f(a) * f(b) > 0:
        a *= 2
        b *= 2

    # Refine the root using bisection
    for _ in range(100):
        mid = (a + b) / 2
        if f(mid) == 0:
            return mid
        if f(a) * f(mid) < 0:
            b = mid
        else:
            a = mid
            
    return (a + b) / 2
