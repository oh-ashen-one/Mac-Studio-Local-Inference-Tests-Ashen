import math


def triangle_area(a, b, c):
    # Check if the sides form a valid triangle
    if a + b <= c or a + c <= b or b + c <= a:
        return -1
    
    # Use Heron's formula to calculate the area
    s = (a + b + c) / 2
    area = math.sqrt(s * (s - a) * (s - b) * (s - c))
    
    # Round to 2 decimal places
    return round(area, 2)
