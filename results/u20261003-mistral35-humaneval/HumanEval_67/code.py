import re

def fruit_distribution(s, n):
    numbers = list(map(int, re.findall(r'\d+', s)))
    return n - sum(numbers)
