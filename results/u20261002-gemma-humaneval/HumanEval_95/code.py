def check_dict_case(dict):
    """
    Given a dictionary, return True if all keys are strings in lower 
    case or all keys are strings in upper case, else return False.
    The function should return False is the given dictionary is empty.
    """
    if not dict:
        return False
    
    keys = list(dict.keys())
    
    # Check if all keys are strings
    if not all(isinstance(k, str) for k in keys):
        return False
    
    # Check if all keys are lowercase
    all_lower = all(k.islower() for k in keys)
    # Check if all keys are uppercase
    all_upper = all(k.isupper() for k in keys)
    
    return all_lower or all_upper
