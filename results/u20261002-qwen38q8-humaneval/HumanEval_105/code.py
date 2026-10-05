def by_length(arr):
    names = {
        1: "One",
        2: "Two",
        3: "Three",
        4: "Four",
        5: "Five",
        6: "Six",
        7: "Seven",
        8: "Eight",
        9: "Nine",
    }
    
    # Filter to only integers between 1 and 9 inclusive
    filtered = [x for x in arr if isinstance(x, int) and 1 <= x <= 9]
    
    # Sort
    filtered.sort()
    
    # Reverse
    filtered.reverse()
    
    # Replace each digit by its corresponding name
    return [names[x] for x in filtered]
