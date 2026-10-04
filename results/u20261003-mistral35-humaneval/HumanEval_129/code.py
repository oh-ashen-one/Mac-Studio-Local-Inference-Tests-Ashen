import heapq

def minPath(grid, k):
    N = len(grid)
    # Each heap element is (current_path, last_row, last_col)
    # We use a tuple for the path to make it comparable in the heap
    heap = []

    # Initialize the heap with all possible starting cells
    for i in range(N):
        for j in range(N):
            heapq.heappush(heap, ([grid[i][j]], i, j))

    # Directions for moving to adjacent cells (up, down, left, right)
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    while heap:
        current_path, i, j = heapq.heappop(heap)
        if len(current_path) == k:
            return current_path
        # Explore all adjacent cells
        for di, dj in directions:
            ni, nj = i + di, j + dj
            if 0 <= ni < N and 0 <= nj < N:
                new_path = current_path + [grid[ni][nj]]
                heapq.heappush(heap, (new_path, ni, nj))
    # In case k is 0, but problem states k is positive, so this line is theoretically unreachable
    return []
