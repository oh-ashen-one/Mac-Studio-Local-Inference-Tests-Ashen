def generate_integers(a, b):
    """
    Given two positive integers a and b, return the even digits between a
    and b, in ascending order.

    For example:
    generate_integers(2, 8) => [2, 4, 6, 8]
    generate_integers(8, 2) => [2, 4, 6, 8]
    generate_integers(10, 14) => []
    """
    # Determine the range
    start = min(a, b)
    end = max(a, b)
    
    # Collect even digits from 0-9 that appear in numbers within the range
    # But wait, re-reading the spec: "return the even digits between a and b"
    # Looking at examples:
    # generate_integers(2, 8) => [2, 4, 6, 8] - these are even numbers between 2 and 8
    # generate_integers(8, 2) => [2, 4, 6, 8] - same, sorted ascending
    # generate_integers(10, 14) => [] - even numbers between 10 and 14 are 10, 12, 14, but result is []
    
    # Hmm, 10, 12, 14 are even numbers between 10 and 14. But the result is [].
    # So it's not about even numbers. It's about even DIGITS.
    
    # Let me re-read: "return the even digits between a and b"
    # For 2 to 8: the even digits that appear in any number from 2 to 8?
    # Numbers 2,3,4,5,6,7,8 contain digits: 2,3,4,5,6,7,8. Even digits: 2,4,6,8.
    # For 10 to 14: numbers 10,11,12,13,14. Digits: 1,0,1,1,1,2,1,3,1,4. Even digits: 0,2,4.
    # But result is [].
    
    # Wait, maybe "even digits" means single-digit even numbers? 0,2,4,6,8?
    # For 10-14, the digits include 0,2,4. But result is [].
    
    # Let me think differently. Maybe it's about which even digits (0,2,4,6,8) are "between" a and b?
    # For 2-8: even digits 2,4,6,8 are all between 2 and 8. Result: [2,4,6,8].
    # For 10-14: even digits 0,2,4,6,8. Which are between 10 and 14? None of 0,2,4,6,8 are between 10 and 14. Result: [].
    
    # That makes sense! The even digits are 0, 2, 4, 6, 8. We return those that fall within [start, end].
    
    even_digits = [0, 2, 4, 6, 8]
    result = [d for d in even_digits if start <= d <= end]
    return result
