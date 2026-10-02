def will_it_fly(q, w):
    """
    Write a function that returns True if the object q will fly, and False otherwise.
    The object q will fly if it's balanced (it is a palindromic list) and the sum of its elements is less than or equal the maximum possible weight w.
    """
    # Check if q is a palindromic list
    if q != q[::-1]:
        return False
    # Check if the sum of elements is less than or equal to w
    if sum(q) <= w:
        return True
    return False
