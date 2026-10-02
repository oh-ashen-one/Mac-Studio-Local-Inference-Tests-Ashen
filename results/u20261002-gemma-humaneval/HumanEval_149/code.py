def sorted_list_sum(lst):
    """Write a function that accepts a list of strings as a parameter,
    deletes the strings that have odd lengths from it,
    and returns the resulted list with a sorted order,
    The list is always a list of strings and never an array of numbers,
    and it may contain duplicates.
    The order of the list should be ascending by length of each word, and you
    should return the list sorted by that rule.
    If two words have the same length, sort the list alphabetically.
    The function should return a list of strings in sorted order.
    """
    # Filter out strings with odd lengths
    filtered_list = [s for s in lst if len(s) % 2 == 0]
    
    # Sort by length (ascending), then alphabetically (ascending)
    filtered_list.sort(key=lambda x: (len(x), x))
    
    return filtered_list
