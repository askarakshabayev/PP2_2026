from itertools import islice

def fib():
    a, b = 0, 1 # a = 0, b = 1
    while True:
        yield a # a = 1
        a, b = b, a + b # a = 3, b = 5

gen = fib()
first_10 = list(islice(gen, 2, 10, 3))
print(first_10)