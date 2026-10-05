def specialFilter(nums):
    count = 0
    for num in nums:
        if abs(num) > 10:
            s = str(abs(num))
            if int(s[0]) % 2 == 1 and int(s[-1]) % 2 == 1:
                count += 1
    return count
