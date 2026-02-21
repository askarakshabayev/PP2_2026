def unpack(data):
    for i in data:
        if isinstance(i, list):
            yield from unpack(i)
        else:
            yield i

data = [[1, 2], 3, [4, 5, [6, 7]], 8]

print(list(unpack(data)))