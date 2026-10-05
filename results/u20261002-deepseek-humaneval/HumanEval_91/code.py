import re

def is_bored(S):
    sentences = re.split(r'[.!?]', S)
    count = 0
    for sentence in sentences:
        stripped = sentence.strip()
        if stripped.startswith('I '):
            count += 1
    return count
