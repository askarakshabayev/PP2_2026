class MyClass:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def sum(self, a, b):
        return self.x + self.y + a + b

a = MyClass(1, 2)
print(a.sum(1, 2))

b = MyClass(2, 3)
print(b.sum(3, 4))