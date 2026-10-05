from collections import deque

def minPath(grid, k):
    """
    Finds the lexicographically smallest path of length k in an N x N grid.
    """
    n = len(grid)
    if k == 1:
        # The smallest path of length 1 is just the minimum value in the grid.
        min_val = min(min(row) for row in grid)
        return [min_val]

    # Find the position of the smallest value in the grid.
    # Since values are 1 to N*N, the smallest is 1.
    start_r, start_c = -1, -1
    for r in range(n):
        for c in range(n):
            if grid[r][c] == 1:
                start_r, start_c = r, c
                break
        if start_r != -1:
            break

    # To get the lexicographically smallest path, we want the smallest possible
    # value at the earliest possible position.
    # The smallest possible starting value is 1.
    # After starting at 1, we want the smallest possible neighbor to visit.
    # If we visit a neighbor 'v', the next step could be back to 1.
    # Thus, the path will look like [1, min_neighbor, 1, min_neighbor, ...]
    
    min_neighbor = float('inf')
    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        nr, nc = start_r + dr, start_c + dc
        if 0 <= nr < n and 0 <= nc < n:
            if grid[nr][nc] < min_neighbor:
                min_neighbor = grid[nr][nc]
    
    path = []
    for i in range(k):
        if i % 2 == 0:
            path.append(1)
        else:
            path.append(min_neighbor)
            
    return path
