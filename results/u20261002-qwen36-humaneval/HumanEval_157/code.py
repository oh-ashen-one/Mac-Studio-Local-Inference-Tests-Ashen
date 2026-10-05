import math

def right_angle_triangle(a, b, c):
    '''
    Given the lengths of the three sides of a triangle. Return True if the three
    sides form a right-angled triangle, False otherwise.
    A right-angled triangle is a triangle in which one angle is right angle or 
    90 degree.
    Example:
    right_angle_triangle(3, 4, 5) == True
    right_angle_triangle(1, 2, 3) == False
    '''
    # Sort the sides so that the largest is last (potential hypotenuse)
    sides = sorted([a, b, c])
    # Check if it's a valid triangle (sum of two smaller sides > largest side)
    if sides[0] + sides[1] <= sides[2]:
        return False
    # Check Pythagorean theorem: a^2 + b^2 = c^2
    # Use a small epsilon for floating point comparison
    epsilon = 1e-9
    return abs(sides[0]**2 + sides[1]**2 - sides[2]**2) < epsilon
