from typing import List

def sort_numbers(numbers: str) -> str:
    numeral_to_value = {
        'zero': 0, 'one': 1, 'two': 2, 'three': 3, 'four': 4,
        'five': 5, 'six': 6, 'seven': 7, 'eight': 8, 'nine': 9
    }
    value_to_numeral = {v: k for k, v in numeral_to_value.items()}
    tokens = numbers.split()
    sorted_values = sorted(numeral_to_value[token] for token in tokens)
    return ' '.join(value_to_numeral[value] for value in sorted_values)
