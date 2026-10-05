import re

def file_name_check(file_name):
    if file_name.count('.') != 1:
        return 'No'

    prefix, suffix = file_name.split('.')

    if not prefix or not prefix[0].isalpha():
        return 'No'

    if suffix not in ['txt', 'exe', 'dll']:
        return 'No'

    digit_count = sum(c.isdigit() for c in file_name)
    if digit_count > 3:
        return 'No'

    return 'Yes'
