def file_name_check(file_name):
    """Create a function which takes a string representing a file's name, and returns
    'Yes' if the the file's name is valid, and returns 'No' otherwise.
    A file's name is considered to be valid if and only if all the following conditions 
    are met:
    - There should not be more than three digits ('0'-'9') in the file's name.
    - The file's name contains exactly one dot '.'
    - The substring before the dot should not be empty, and it starts with a letter from 
    the latin alphapet ('a'-'z' and 'A'-'Z').
    - The substring after the dot should be one of these: ['txt', 'exe', 'dll']
    """
    # Check for more than three digits
    digit_count = sum(c.isdigit() for c in file_name)
    if digit_count > 3:
        return 'No'
    
    # Check for exactly one dot
    if file_name.count('.') != 1:
        return 'No'
    
    # Split into name and extension
    name_part, ext_part = file_name.split('.')
    
    # Check if name part is empty or doesn't start with a latin letter
    if not name_part or not name_part[0].isalpha():
        return 'No'
    
    # Check if extension is valid
    if ext_part not in ['txt', 'exe', 'dll']:
        return 'No'
    
    return 'Yes'
