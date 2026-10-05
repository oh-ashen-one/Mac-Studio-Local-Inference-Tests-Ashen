def decimal_to_binary(decimal):
    """Convert a decimal number to a binary string with 'db' prefix and suffix."""
    binary_str = bin(decimal)[2:]  # Get binary without '0b' prefix
    return f"db{binary_str}db"
