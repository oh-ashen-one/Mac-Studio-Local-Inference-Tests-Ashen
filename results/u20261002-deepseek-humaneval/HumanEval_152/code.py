from typing import List

def compare(game: List[int], guess: List[int]) -> List[int]:
    return [abs(g - s) for s, g in zip(game, guess)]
