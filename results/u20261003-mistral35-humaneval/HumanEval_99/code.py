import math

def closest_integer(value):
    num = float(value)
    if num >= 0:
        return math.floor(num + 0.5)
    else:
        return math.ceil(num - 0.5)
