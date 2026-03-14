a = [1, 2, 3, 4, 5]
b = [2, 3, 4, 5, 6]

c = list(map(lambda x, y: x + y, a, b))
print(c)