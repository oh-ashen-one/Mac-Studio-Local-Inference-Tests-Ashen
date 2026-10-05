def compare(game, guess):
    """
    Determine how far off each guess was from the actual score.
    
    Args:
        game: List of actual scores for each match.
        guess: List of guessed scores for each match.
    
    Returns:
        List of absolute differences between each guess and the corresponding score.
        If the guess is correct, the value is 0.
    """
    return [abs(g - p) for g, p in zip(game, guess)]
