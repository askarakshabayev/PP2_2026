def my_generator():
    print("first")
    yield 1
    print("second")
    yield 2
    print("third")
    yield 3


a = my_generator()
print(next(a))
print(next(a))
print(next(a))
print(next(a))
