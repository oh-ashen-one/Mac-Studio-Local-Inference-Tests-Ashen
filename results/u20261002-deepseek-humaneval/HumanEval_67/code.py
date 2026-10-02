import re

def fruit_distribution(s, n):
    numbers = [int(x) for x in re.findall(r'\d+', s)]
    return n - sum(numbers)
