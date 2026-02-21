def my_generator():
    print("first")
    yield 1
    print("second")
    yield 2
    print("third")
    yield 3

gen = my_generator()
print(next(gen))
print(next(gen))
print(next(gen))
print(next(gen))
