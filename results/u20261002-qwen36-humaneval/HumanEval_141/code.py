import re
from typing import List


def file_name_check(file_name: str) -> str:
    """
    Check if a file name is valid based on the following rules:
    - No more than three digits ('0'-'9') in the file name.
    - Exactly one dot '.' in the file name.
    - The substring before the dot is not empty and starts with a Latin alphabet letter.
    - The substring after the dot is one of: 'txt', 'exe', 'dll'.
    
    Returns 'Yes' if valid, 'No' otherwise.
    """
    # Check for exactly one dot
    if file_name.count('.') != 1:
        return 'No'
    
    # Split by the dot
    parts = file_name.split('.')
    if len(parts) != 2:
        return 'No'
    
    name_part = parts[0]
    extension_part = parts[1]
    
    # Check that the name part is not empty
    if not name_part:
        return 'No'
    
    # Check that the name part starts with a Latin alphabet letter
    if not name_part[0].isalpha() or not (name_part[0].isascii() and (name_part[0].islower() or name_part[0].isupper())):
        return 'No'
    
    # Check that the extension is one of the allowed ones
    if extension_part not in ['txt', 'exe', 'dll']:
        return 'No'
    
    # Count digits in the entire file name
    digit_count = sum(1 for c in file_name if c.isdigit())
    if digit_count > 3:
        return 'No'
    
    return 'Yes'
