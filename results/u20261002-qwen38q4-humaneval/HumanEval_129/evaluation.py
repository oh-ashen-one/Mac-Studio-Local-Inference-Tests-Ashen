import ast as _bench_ast
import operator as _bench_operator
def _bench_arithmetic_node(n):
    if isinstance(n, _bench_ast.Constant) and type(n.value) in (int, float): return n.value
    if isinstance(n, _bench_ast.UnaryOp) and isinstance(n.op, (_bench_ast.UAdd, _bench_ast.USub)):
        v = _bench_arithmetic_node(n.operand)
        return v if isinstance(n.op, _bench_ast.UAdd) else -v
    ops = {_bench_ast.Add: _bench_operator.add, _bench_ast.Sub: _bench_operator.sub, _bench_ast.Mult: _bench_operator.mul, _bench_ast.Div: _bench_operator.truediv, _bench_ast.FloorDiv: _bench_operator.floordiv, _bench_ast.Mod: _bench_operator.mod, _bench_ast.Pow: _bench_operator.pow}
    if isinstance(n, _bench_ast.BinOp) and type(n.op) in ops:
        return ops[type(n.op)](_bench_arithmetic_node(n.left), _bench_arithmetic_node(n.right))
    raise ValueError('Only numeric arithmetic is permitted by benchmark eval')
def eval(expression):
    return _bench_arithmetic_node(_bench_ast.parse(expression, mode='eval').body)


def minPath(grid, k):
    """
    Given a grid with N rows and N columns (N >= 2) and a positive integer k, 
    each cell of the grid contains a value. Every integer in the range [1, N * N]
    inclusive appears exactly once on the cells of the grid.

    You have to find the minimum path of length k in the grid. You can start
    from any cell, and in each step you can move to any of the neighbor cells,
    in other words, you can go to cells which share an edge with you current
    cell.
    Please note that a path of length k means visiting exactly k cells (not
    necessarily distinct).
    You CANNOT go off the grid.
    A path A (of length k) is considered less than a path B (of length k) if
    after making the ordered lists of the values on the cells that A and B go
    through (let's call them lst_A and lst_B), lst_A is lexicographically less
    than lst_B, in other words, there exist an integer index i (1 <= i <= k)
    such that lst_A[i] < lst_B[i] and for any j (1 <= j < i) we have
    lst_A[j] = lst_B[j].
    It is guaranteed that the answer is unique.
    Return an ordered list of the values on the cells that the minimum path go through.

    Examples:

        Input: grid = [ [1,2,3], [4,5,6], [7,8,9]], k = 3
        Output: [1, 2, 1]

        Input: grid = [ [5,9,3], [4,1,6], [7,8,2]], k = 1
        Output: [1]
    """

from collections import deque
from typing import List

def minPath(grid: List[List[int]], k: int) -> List[int]:
    n = len(grid)
    if n == 0:
        return []
    
    # Find the cell with value 1 (the smallest possible starting value)
    # Since we want lexicographically smallest path, we should start from the smallest possible value.
    # But wait - we can start from ANY cell. The lexicographically smallest path will start with the smallest possible first element.
    # The smallest value in the grid is 1, so the optimal path must start at the cell with value 1.
    
    # Find position of value 1
    start_pos = None
    for i in range(n):
        for j in range(n):
            if grid[i][j] == 1:
                start_pos = (i, j)
                break
        if start_pos:
            break
    
    if start_pos is None:
        return []
    
    # Now we need to find the lexicographically smallest path of length k starting from start_pos.
    # At each step, we can move to any neighbor (up, down, left, right) or stay? No, we move to neighbor cells.
    # Wait, re-reading: "in each step you can move to any of the neighbor cells" - so we must move to a neighbor.
    # But the path visits exactly k cells. So we start at cell 1 (step 1), then move to a neighbor (step 2), etc.
    
    # We need to find the lexicographically smallest sequence of k values.
    # Since we start at value 1, the first element is fixed as 1.
    # For the second element, we want the smallest possible value among all neighbors of the start cell.
    # For the third element, given the second element's position, we want the smallest possible value among its neighbors, etc.
    
    # However, this greedy approach might not work because choosing a slightly larger value at step 2 might lead to a much smaller value at step 3.
    # But wait - lexicographic comparison means we prioritize earlier positions. So we should greedily choose the smallest possible value at each step.
    
    # Actually, let me think again. The lexicographically smallest path is determined by:
    # 1. First element: must be 1 (smallest possible)
    # 2. Second element: smallest value among neighbors of the cell with value 1
    # 3. Third element: smallest value among neighbors of the cell chosen in step 2
    # ... and so on.
    
    # This greedy approach works because lexicographic order prioritizes earlier elements.
    # If we can choose a smaller value at position i, it doesn't matter what happens at position i+1 or later.
    
    # But wait - there's a subtlety. At each step, we're at a specific cell. The next value is determined by which neighbor we move to.
    # So at each step, given our current position, we choose the neighbor with the smallest value.
    
    # Let's implement this greedy approach.
    
    path = [1]
    current_pos = start_pos
    
    for _ in range(k - 1):
        i, j = current_pos
        # Get all neighbors
        neighbors = []
        if i > 0:
            neighbors.append((i - 1, j))
        if i < n - 1:
            neighbors.append((i + 1, j))
        if j > 0:
            neighbors.append((i, j - 1))
        if j < n - 1:
            neighbors.append((i, j + 1))
        
        # Find the neighbor with the smallest value
        min_val = float('inf')
        min_pos = None
        for ni, nj in neighbors:
            val = grid[ni][nj]
            if val < min_val:
                min_val = val
                min_pos = (ni, nj)
        
        path.append(min_val)
        current_pos = min_pos
    
    return path

def check(candidate):

    # Check some simple cases
    print
    assert candidate([[1, 2, 3], [4, 5, 6], [7, 8, 9]], 3) == [1, 2, 1]
    assert candidate([[5, 9, 3], [4, 1, 6], [7, 8, 2]], 1) == [1]
    assert candidate([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16]], 4) == [1, 2, 1, 2]
    assert candidate([[6, 4, 13, 10], [5, 7, 12, 1], [3, 16, 11, 15], [8, 14, 9, 2]], 7) == [1, 10, 1, 10, 1, 10, 1]
    assert candidate([[8, 14, 9, 2], [6, 4, 13, 15], [5, 7, 1, 12], [3, 10, 11, 16]], 5) == [1, 7, 1, 7, 1]
    assert candidate([[11, 8, 7, 2], [5, 16, 14, 4], [9, 3, 15, 6], [12, 13, 10, 1]], 9) == [1, 6, 1, 6, 1, 6, 1, 6, 1]
    assert candidate([[12, 13, 10, 1], [9, 3, 15, 6], [5, 16, 14, 4], [11, 8, 7, 2]], 12) == [1, 6, 1, 6, 1, 6, 1, 6, 1, 6, 1, 6]
    assert candidate([[2, 7, 4], [3, 1, 5], [6, 8, 9]], 8) == [1, 3, 1, 3, 1, 3, 1, 3]
    assert candidate([[6, 1, 5], [3, 8, 9], [2, 7, 4]], 8) == [1, 5, 1, 5, 1, 5, 1, 5]

    # Check some edge cases that are easy to work out by hand.
    assert candidate([[1, 2], [3, 4]], 10) == [1, 2, 1, 2, 1, 2, 1, 2, 1, 2]
    assert candidate([[1, 3], [3, 2]], 10) == [1, 3, 1, 3, 1, 3, 1, 3, 1, 3]


check(minPath)
print('PASS_625c2f32d31a49efb82397fdefe294b7')
