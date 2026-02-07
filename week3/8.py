a = [1, 2, 3, 1, 2, 3, 1, 1, 2, 2, 3]

d = dict()

for i in a:
    if i not in d:
        d[i] = 0
    d[i] += 1

# d.pop(1)

for key in d:
    print(key, d[key])

# print(d.keys())
# print(d.values())
# print(d.items())

# for key, value in d.items():
#     print(key, value)

# print(d.get(4, 0))
