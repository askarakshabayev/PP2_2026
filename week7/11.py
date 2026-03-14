a = [2, 4, 6, 8, 10, 1]



print(any(x % 2 == 0 for x in a))
print(all(x % 2 == 0 for x in a))