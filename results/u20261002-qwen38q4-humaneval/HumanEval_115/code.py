def max_fill(grid, capacity):
    import math
    total_drops = 0
    for row in grid:
        water_in_row = sum(row)
        if water_in_row > 0:
            total_drops += math.ceil(water_in_row / capacity)
    return total_drops
