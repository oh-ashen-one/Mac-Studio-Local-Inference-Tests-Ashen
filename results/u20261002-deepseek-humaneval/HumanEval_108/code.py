def count_nums(arr):
    count = 0
    for num in arr:
        if num < 0:
            digits = list(str(num)[1:])
            signed_sum = -int(digits[0]) + sum(int(d) for d in digits[1:])
        else:
            signed_sum = sum(int(d) for d in str(num))
        if signed_sum > 0:
            count += 1
    return count
