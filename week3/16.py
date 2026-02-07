def func(a, b, *args, **kwargs):
    print(a)
    print("------------------------------------")
    print(b)
    print("------------------------------------")
    print(args)
    print("------------------------------------")
    print(kwargs)

# func(name="Askar", sname="Akshabayev")
func("hello", 5, 1, 2, 3, 4, 5, "world", name="Askar", sname="Akshabayev")