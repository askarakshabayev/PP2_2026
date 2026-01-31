a = [1, 2, 3]
b = a.copy()

print(hex(id(a)))
print(hex(id(b)))

b.append(4)
print(a)
print(b)