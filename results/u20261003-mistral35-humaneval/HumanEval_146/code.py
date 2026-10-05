def specialFilter(nums):
    count = 0
    for num in nums:
        if num > 10:
            s = str(abs(num))
            if len(s) > 0 and int(s[0]) % 2 != 0 and int(s[-1]) % 2 != 0:
                count += 1
    return count
