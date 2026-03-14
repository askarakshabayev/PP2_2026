a = [10, 12, 7, 20, 6, 8]
# 10 -> 1, 2, 5, 10 (4)
# 20 -> 1, 2, 4, 5, 10, 20 (6)
# 7 -> 1, 7 (2)
# 12 -> 1, 2, 3, 4, 6, 12 (6)
# 6 -> 1, 2, 3, 6 (4)
# 8 -> 1, 2, 4, 8 (4)

def func(x):
    p = 0
    for i in range(1, x + 1):
        if x % i == 0:
            p += 1
    return (p, x)

mini = min(a, key=func)
maxi = max(a, key=func)

print(mini, maxi)