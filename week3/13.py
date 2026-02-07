def func(a, *args):
    for i in args:
        print(i, type(i))

# func([1, 2, 3], "hello", 10, 20)
# a = [1, 2, 3]
# args = ["hello", 10, 20]

func(1, 2, 3, 4, 5)