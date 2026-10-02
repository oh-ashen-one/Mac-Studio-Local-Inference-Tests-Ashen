def get_row(lst, x):
    """
    You are given a 2 dimensional data, as a nested lists,
    which is similar to matrix, however, unlike matrices,
    each row may contain a different number of columns.
    Given lst, and integer x, find integers x in the list,
    and return list of tuples, [(x1, y1), (x2, y2) ...] such that
    each tuple is a coordinate - (row, columns), starting with 0.
    Sort coordinates initially by rows in ascending order.
    Also, sort coordinates of the row by columns in descending order.
    """
    result = []
    for row_idx, row in enumerate(lst):
        # Find all column indices where the value is x
        cols = [col_idx for col_idx, val in enumerate(row) if val == x]
        # Sort column indices in descending order for the current row
        cols.sort(reverse=True)
        # Append as tuples (row, col)
        for col_idx in cols:
            result.append((row_idx, col_idx))
    
    return result
