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
