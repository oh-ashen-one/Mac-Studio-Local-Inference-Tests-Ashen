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
    # Bisection method to find a root of the polynomial.
    # The problem guarantees a solution exists.
    # We search in a sufficiently large interval.
    a, b = -1e6, 1e6
    fa, fb = poly(xs, a), poly(xs, b)

    # Expand the interval if necessary to find a sign change
    while fa * fb > 0:
        a *= 2
        b *= 2
        fa, fb = poly(xs, a), poly(xs, b)
        if abs(a) > 1e15:
            break

    # Perform bisection
    for _ in range(100):
        mid = (a + b) / 2
        fmid = poly(xs, mid)
        if fmid == 0:
            return mid
        if fa * fmid < 0:
            b = mid
            fb = fmid
        else:
            a = mid
            fa = fmid

    return (a + b) / 2
