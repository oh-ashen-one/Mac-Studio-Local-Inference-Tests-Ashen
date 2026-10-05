def total_match(lst1, lst2):
    '''
    Write a function that accepts two lists of strings and returns the list that has 
    total number of chars in the all strings of the list less than the other list.

    if the two lists have the same number of chars, return the first list.
    '''
    len1 = sum(len(s) for s in lst1)
    len2 = sum(len(s) for s in lst2)
    
    if len1 <= len2:
        return lst1
    else:
        return lst2
