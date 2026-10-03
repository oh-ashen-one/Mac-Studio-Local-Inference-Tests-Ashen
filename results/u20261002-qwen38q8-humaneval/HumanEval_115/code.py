def max_fill(grid, capacity):
    import math
    total_drops = 0
    for row in grid:
        total_drops += sum(row)
    return math.ceil(total_drops / capacity)
