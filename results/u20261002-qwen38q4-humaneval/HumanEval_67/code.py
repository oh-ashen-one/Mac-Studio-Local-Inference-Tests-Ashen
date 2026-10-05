def fruit_distribution(s, n):
    """
    In this task, you will be given a string that represents a number of apples and oranges 
    that are distributed in a basket of fruit this basket contains 
    apples, oranges, and mango fruits. Given the string that represents the total number of 
    the oranges and apples and an integer that represent the total number of the fruits 
    in the basket return the number of the mango fruits in the basket.
    for examble:
    fruit_distribution("5 apples and 6 oranges", 19) ->19 - 5 - 6 = 8
    fruit_distribution("0 apples and 1 oranges",3) -> 3 - 0 - 1 = 2
    fruit_distribution("2 apples and 3 oranges", 100) -> 100 - 2 - 3 = 95
    fruit_distribution("100 apples and 1 oranges",120) -> 120 - 100 - 1 = 19
    """
    # Extract the numbers from the string
    # The string format is like "X apples and Y oranges"
    # We need to find the two numbers
    
    # Split by spaces and find the numeric parts
    parts = s.split()
    apples = 0
    oranges = 0
    
    for i, part in enumerate(parts):
        if part.isdigit():
            # Check what follows this number
            if i + 1 < len(parts):
                next_word = parts[i + 1]
                if next_word == 'apples':
                    apples = int(part)
                elif next_word == 'oranges':
                    oranges = int(part)
    
    return n - apples - oranges
