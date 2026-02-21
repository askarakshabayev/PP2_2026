def numbers(n):
    for i in range(1, n + 1):
        yield i

def doubled(gen):
    for value in gen:
        yield value * 2

def only_greater_than(gen, threshold):
    for value in gen:
        if value > threshold:
            yield value

# Pipeline: numbers -> double -> filter > 10
pipeline = only_greater_than(doubled(numbers(10)), 10)
print(list(pipeline))  # [12, 14, 16, 18, 20]
