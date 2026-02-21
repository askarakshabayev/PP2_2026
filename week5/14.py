# a = [1, 2, [2, 3, 4], [5, 6, [7, 8]], 10]
# b = [1, 2, 2, 3, 4, 5, 6, 7, 8, 10]

def func(data):
    for i in data: # 10
        if isinstance(i, list):
            yield from func(i)
        else:
            yield i

a = [1, 2, [2, 3, 4], [5, 6, [7, 8]], 10]
print(list(func(a)))



