from collections import deque

def minPath(grid, k):
    N = len(grid)
    
    # Find the position of the minimum value (1) in the grid
    start_r, start_c = -1, -1
    for r in range(N):
        for c in range(N):
            if grid[r][c] == 1:
                start_r, start_c = r, c
                break
        if start_r != -1:
            break

    # BFS initialization
    # State: (current_row, current_col, path_list)
    # We start with the path containing the minimum value.
    initial_path = [grid[start_r][start_c]]
    queue = deque([(start_r, start_c, initial_path)])
    
    # Directions: Up, Down, Left, Right
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    while queue:
        r, c, path = queue.popleft()
        
        # If we have reached the required length, return the path
        if len(path) == k:
            return path
        
        # Explore neighbors
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            
            # Check boundaries
            if 0 <= nr < N and 0 <= nc < N:
                new_path = path + [grid[nr][nc]]
                queue.append((nr, nc, new_path))
                
    return []
