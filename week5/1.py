class MyClass:
    x = 5
    y = 6

    def sum(self, a, b):
        return self.x + self.y + a + b

a = MyClass()
a.x = 10
a.y = 20
print(a.x)
print(a.y)
print(a.sum(1, 2))

b = MyClass()
print(b.x)
print(b.y)
print(b.sum(3, 4))