import math
from typing import List


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
    # Use Newton's method to find a root
    # Start with an initial guess
    # For a polynomial, we can try multiple starting points
    
    def derivative(xs: list) -> list:
        """Compute the derivative coefficients."""
        if len(xs) <= 1:
            return [0.0]
        return [i * xs[i] for i in range(1, len(xs))]
    
    def poly_val(xs: list, x: float) -> float:
        """Evaluate polynomial at x."""
        result = 0.0
        for i, coeff in enumerate(xs):
            result += coeff * (x ** i)
        return result
    
    def deriv_val(xs: list, x: float) -> float:
        """Evaluate derivative at x."""
        deriv_coeffs = derivative(xs)
        return poly_val(deriv_coeffs, x)
    
    # Try multiple initial guesses to find a root
    initial_guesses = [-100, -10, -1, 0, 1, 10, 100]
    
    for guess in initial_guesses:
        x = guess
        for _ in range(1000):  # Max iterations
            fx = poly_val(xs, x)
            if abs(fx) < 1e-10:
                return x
            dfx = deriv_val(xs, x)
            if abs(dfx) < 1e-15:
                # Derivative is too small, skip this guess
                break
            x = x - fx / dfx
        else:
            # Check if we converged
            if abs(poly_val(xs, x)) < 1e-10:
                return x
    
    # If Newton's method didn't work, try bisection or other methods
    # Find a range where the sign changes
    # Since the problem guarantees a solution, let's try a broader search
    
    # Try scanning for sign changes
    low = -1000.0
    high = 1000.0
    
    # Binary search / bisection approach
    # Find an interval [a, b] where poly(a) and poly(b) have opposite signs
    
    # First, let's try to find such an interval
    step = 0.1
    a = -1000.0
    fa = poly_val(xs, a)
    
    b = a + step
    fb = poly_val(xs, b)
    
    while abs(fa) > 1e-10 and abs(fb) > 1e-10:
        if fa * fb < 0:
            # Sign change found, use bisection
            for _ in range(100):
                mid = (a + b) / 2.0
                fmid = poly_val(xs, mid)
                if abs(fmid) < 1e-10:
                    return mid
                if fa * fmid < 0:
                    b = mid
                    fb = fmid
                else:
                    a = mid
                    fa = fmid
            return (a + b) / 2.0
        a = b
        fa = fb
        b += step
        fb = poly_val(xs, b)
        if b > 10000:
            break
    
    # Fallback: return a value that makes poly close to 0
    # Try the initial guesses again with more iterations
    for guess in initial_guesses:
        x = guess
        for _ in range(10000):
            fx = poly_val(xs, x)
            if abs(fx) < 1e-10:
                return x
            dfx = deriv_val(xs, x)
            if abs(dfx) < 1e-15:
                break
            x = x - fx / dfx
        if abs(poly_val(xs, x)) < 1e-8:
            return x
    
    # Last resort: return 0
    return 0.0
