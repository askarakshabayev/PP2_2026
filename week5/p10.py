def number(n):
    for i in range(n):
        yield i

def double(gen):
    for i in gen:
        yield i * 2

def only_greater_than(gen, threshold):
    for i in gen:
        if i > threshold:
            yield i

pipeline = only_greater_than(double(number(10)), 10)
print(list(pipeline))

