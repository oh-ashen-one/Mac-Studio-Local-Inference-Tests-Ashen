import re

def fruit_distribution(s, n):
    """
    In this task, you will be given a string that represents a number of apples and oranges 
    that are distributed in a basket of fruit this basket contains 
    apples, oranges, and mango fruits. Given the string that represents the total number of 
    the oranges and apples and an integer that represent the total number of the fruits 
    in the basket return the number of the mango fruits in the basket.
    """
    # Find all sequences of digits in the string
    numbers = re.findall(r'\d+', s)
    # Convert the found strings to integers
    counts = [int(num) for num in numbers]
    # Subtract the sum of apples and oranges from the total number of fruits
    return n - sum(counts)
