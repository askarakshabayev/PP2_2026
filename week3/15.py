def find_min(a, b, c):
    if a <= b and a <= c:
        return a
    if b <= a and b <= c:
        return b
    return c

mini = find_min(19, 6, 10)

mini = find_mini(find_mini(1, 2, 3), find_mini(2, 3, 4), find_mini(5, 4, 3))
print(mini)