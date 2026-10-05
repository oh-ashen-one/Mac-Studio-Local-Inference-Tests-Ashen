def check_dict_case(dict):
    if not dict:
        return False
    keys = list(dict.keys())
    if all(isinstance(k, str) and k.islower() for k in keys):
        return True
    if all(isinstance(k, str) and k.isupper() for k in keys):
        return True
    return False
