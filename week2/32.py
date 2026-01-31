fruits = ["apple", "banana", "cherry"]

l = [x.upper() for x in fruits]

print(l)

a = [x if x % 2 == 0 for x in range(20)]
print(a)