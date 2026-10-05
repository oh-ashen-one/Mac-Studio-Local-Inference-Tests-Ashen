def exchange(lst1, lst2):
    """In this problem, you will implement a function that takes two lists of numbers,
    and determines whether it is possible to perform an exchange of elements
    between them to make lst1 a list of only even numbers.
    There is no limit on the number of exchanged elements between lst1 and lst2.
    If it is possible to exchange elements between the lst1 and lst2 to make
    all the elements of lst1 to be even, return "YES".
    Otherwise, return "NO".
    For example:
    exchange([1, 2, 3, 4], [1, 2, 3, 4]) => "YES"
    exchange([1, 2, 3, 4], [1, 5, 3, 4]) => "NO"
    It is assumed that the input lists will be non-empty.
    """
    # Count the number of odd elements in lst1
    odd_in_lst1 = sum(1 for x in lst1 if x % 2 != 0)

    # If there are no odd elements, no exchange is needed
    if odd_in_lst1 == 0:
        return "YES"

    # Count the number of even elements in lst2
    even_in_lst2 = sum(1 for x in lst2 if x % 2 == 0)

    # If lst2 has enough even elements to replace all odd elements in lst1
    if even_in_lst2 >= odd_in_lst1:
        return "YES"
    else:
        return "NO"
