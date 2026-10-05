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

    Examples:

        Input: grid = [ [1,2,3], [4,5,6], [7,8,9]], k = 3
        Output: [1, 2, 1]

        Input: grid = [ [5,9,3], [4,1,6], [7,8,2]], k = 1
        Output: [1]
    """
    N = len(grid)
    
    # Find all cells and their values
    # We need to find the lexicographically smallest path of length k
    
    # Since k can be large, we need an efficient approach.
    # Key insight: The first element of the path determines the starting cell.
    # To get the lexicographically smallest path, we should start with the smallest possible value.
    # But we also need to consider subsequent elements.
    
    # Approach: Use BFS/priority queue based search.
    # State: (current_path_so_far, current_cell)
    # But storing full paths is expensive.
    
    # Alternative: Since we want the lexicographically smallest path,
    # we can think of it as: among all paths of length k, find the one that is lex smallest.
    
    # Let's use a priority queue where we explore paths in lex order.
    # Each state in PQ: (path_tuple, r, c)
    # But path_tuple can be long. However, k might be up to N*N or more?
    # The problem doesn't specify bounds on k, but since we revisit cells, k can be large.
    
    # Actually, let's think differently. The minimum path starts with the minimum value in the grid.
    # Let min_val = 1 (since values are 1 to N*N).
    # Find all cells with value 1. For each such cell, we need to find the lex smallest path of length k starting from it.
    # Then among all such paths, pick the lex smallest.
    
    # But wait, the first element is 1 for all such paths. So we need to compare the second element, etc.
    
    # Let's use Dijkstra-like approach with priority queue.
    # Priority: the path so far (as a tuple).
    # We start with all cells that have the minimum value (which is 1).
    # For each starting cell with value 1, we push ( [grid[r][c]], r, c ) into the PQ.
    # Then we pop the smallest path, and if its length is k, we return it.
    # Otherwise, we extend it to neighbors.
    
    # But this could be very slow if k is large.
    
    # Let's think about the constraints. N >= 2, k is a positive integer.
    # The grid has N*N cells with values 1 to N*N.
    
    # Key observation: The lex smallest path will start with the smallest value in the grid, which is 1.
    # If there are multiple cells with value 1, we need to check all of them.
    # But since 1 appears exactly once, there's only one cell with value 1.
    # Wait, "Every integer in the range [1, N * N] inclusive appears exactly once on the cells of the grid."
    # So value 1 appears exactly once. So the first element of the minimum path must be 1.
    
    # So we find the cell (r0, c0) where grid[r0][c0] == 1.
    # Then we need to find the lex smallest path of length k starting from (r0, c0).
    
    # Now, from (r0, c0), we can move to any neighbor. We want the lex smallest sequence of k values.
    # This is equivalent to: at each step, choose the neighbor with the smallest value, but we need to look ahead.
    
    # Actually, this is a shortest path problem in a graph where edges have weights (the values of the destination cells),
    # and we want the lex smallest path of exactly k steps.
    
    # Let's use BFS with priority queue.
    # State: (path_so_far, r, c)
    # We start with path = [1], r = r0, c = c0.
    # PQ ordered by path_so_far.
    
    # Since k can be large, this might be too slow. But let's try it for reasonable k.
    
    # Find the position of 1
    start_r, start_c = -1, -1
    for r in range(N):
        for c in range(N):
            if grid[r][c] == 1:
                start_r, start_c = r, c
                break
        if start_r != -1:
            break
    
    # If k == 1, return [1]
    if k == 1:
        return [1]
    
    # Use priority queue: (path_tuple, r, c)
    # path_tuple is the sequence of values so far.
    pq = []
    heapq.heappush(pq, ([grid[start_r][start_c]], start_r, start_c))
    
    while pq:
        path, r, c = heapq.heappop(pq)
        
        if len(path) == k:
            return path
        
        # Extend to neighbors
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < N and 0 <= nc < N:
                new_path = path + [grid[nr][nc]]
                heapq.heappush(pq, (new_path, nr, nc))
    
    # Should not reach here
    return []
