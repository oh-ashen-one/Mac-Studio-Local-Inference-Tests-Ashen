from heapq import heappush, heappop

def minPath(grid, k):
    n = len(grid)
    if k == 1:
        return [min(min(row) for row in grid)]
    
    # Precompute positions of each value
    pos = {}
    for i in range(n):
        for j in range(n):
            pos[grid[i][j]] = (i, j)
    
    # Start from the smallest value
    start_val = min(pos)
    start_i, start_j = pos[start_val]
    
    # Dijkstra-like search on state (value, i, j, length)
    # We want lexicographically smallest sequence, so we use a priority queue
    # where the priority is the sequence itself (as tuple)
    pq = []
    heappush(pq, (start_val, start_i, start_j, 1, (start_val,)))
    
    visited = {}
    
    while pq:
        val, i, j, length, seq = heappop(pq)
        if length == k:
            return list(seq)
        
        key = (i, j, length)
        if key in visited and visited[key] <= seq:
            continue
        visited[key] = seq
        
        for di, dj in [(1,0),(-1,0),(0,1),(0,-1)]:
            ni, nj = i+di, j+dj
            if 0 <= ni < n and 0 <= nj < n:
                nval = grid[ni][nj]
                nseq = seq + (nval,)
                heappush(pq, (nval, ni, nj, length+1, nseq))
    
    return []
