x = 1
def func():
    global x
    x = 2

func()
print(x)