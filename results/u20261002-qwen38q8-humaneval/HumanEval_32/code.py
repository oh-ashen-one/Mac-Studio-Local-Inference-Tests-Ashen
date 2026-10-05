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
    # Let's try to find a sign change by scanning
    
    # Try smaller ranges first
    found = False
    for scale in [1, 10, 100, 1000, 10000]:
        a = -scale
        b = scale
        fa = poly(xs, a)
        fb = poly(xs, b)
        if fa * fb <= 0:
            found = True
            break
    
    if not found:
        # Try to find a sign change by scanning
        a = -10000.0
        b = 10000.0
        n_steps = 10000
        step = (b - a) / n_steps
        prev_x = a
        prev_f = poly(xs, a)
        for i in range(1, n_steps + 1):
            curr_x = a + i * step
            curr_f = poly(xs, curr_x)
            if prev_f * curr_f <= 0:
                a = prev_x
                b = curr_x
                found = True
                break
            prev_x = curr_x
            prev_f = curr_f
    
    if not found:
        # Fallback: try Newton's method from a few starting points
        # Or just return 0.0 as a last resort
        # Let's try Newton's method
        x = 1.0
        for _ in range(1000):
            fx = poly(xs, x)
            if abs(fx) < 1e-10:
                break
            # Compute derivative
            dfx = sum([coeff * (i + 1) * math.pow(x, i) for i, coeff in enumerate(xs[1:])]) if len(xs) > 1 else 0
            if abs(dfx) < 1e-15:
                x += 0.1
                continue
            x_new = x - fx / dfx
            if abs(x_new - x) < 1e-10:
                x = x_new
                break
            x = x_new
        return x
    
    # Bisection method
    fa = poly(xs, a)
    fb = poly(xs, b)
    
    # If fa is zero, return a
    if abs(fa) < 1e-10:
        return a
    if abs(fb) < 1e-10:
        return b
    
    for _ in range(1000):
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
