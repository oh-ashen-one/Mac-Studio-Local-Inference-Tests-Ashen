from collections import deque
import heapq

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
    """
    n = len(grid)
    
    # Find the position of each value
    pos = {}
    for i in range(n):
        for j in range(n):
            pos[grid[i][j]] = (i, j)
    
    # We want to find the lexicographically smallest path of length k.
    # The first element should be the smallest possible value, which is 1.
    # Then from the cell containing 1, we want the smallest possible next value, etc.
    
    # However, we need to be careful: the path must be valid (consecutive cells must be adjacent).
    # So we do a BFS/DFS-like approach but always choosing the smallest next value that is reachable.
    
    # Actually, since we want lexicographically smallest, we can greedily choose:
    # Step 1: Start at the cell with value 1 (since 1 is the smallest value, and we can start anywhere).
    # Step 2: From current cell, look at all neighbors, pick the one with the smallest value.
    # But wait - this greedy approach might not work because we need to ensure we can complete the path of length k.
    # However, since we can revisit cells, and the grid is connected, from any cell we can always continue.
    # But the greedy choice of smallest neighbor might lead to a dead end in terms of lexicographic optimality?
    # No, because lexicographic order is determined by the first differing element. So at each step, we should pick the smallest possible next value.
    
    # Let me reconsider: The path is a sequence of k cells. We want the lexicographically smallest sequence.
    # The first element: we can start at any cell, so we pick the cell with the smallest value, which is 1.
    # The second element: from the cell with value 1, we can move to any neighbor. We pick the neighbor with the smallest value.
    # The third element: from the cell we just moved to, we pick the neighbor with the smallest value, and so on.
    
    # This greedy approach should work because:
    # - At each step, the choice of the next cell only depends on the current cell.
    # - We want to minimize the sequence lexicographically, so at each position, we want the smallest possible value.
    # - Since we can revisit cells, there's no constraint that prevents us from always being able to continue.
    
    # Let's implement this greedy approach.
    
    # Start at the cell with value 1
    current_pos = pos[1]
    path = [1]
    
    for _ in range(k - 1):
        i, j = current_pos
        # Find all neighbors
        neighbors = []
        for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            ni, nj = i + di, j + dj
            if 0 <= ni < n and 0 <= nj < n:
                neighbors.append((grid[ni][nj], ni, nj))
        
        # Pick the neighbor with the smallest value
        neighbors.sort(key=lambda x: x[0])
        min_val, ni, nj = neighbors[0]
        path.append(min_val)
        current_pos = (ni, nj)
    
    return path
