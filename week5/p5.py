import math
from itertools import islice

class CountDown:

    def __init__(self, start):
        self.current = start

    def __iter__(self):
        return self

    def __next__(self):
        if self.current < 0:
            raise StopIteration
        value = self.current
        self.current -= 1
        return value

class EvenNumberIterator:

    def __init__(self, start):
        self.current = start

    def __iter__(self):
        return self

    def __next__(self):
        value = self.current
        self.current += 2
        return value

class EvenNumbers:

    def __init__(self):
        self.current = 2

    def next_prime(self):
        found = False
        while not found:
            found = True
            self.current += 1
            for i in range(2, int(math.sqrt(self.current)) + 1):
                if self.current % i == 0:
                    found = False
                    break
        return self.current

    def __iter__(self):
        return self

    def __next__(self):
        value = self.current
        self.current = self.next_prime()
        return value


# a = CountDown(10)
# it = iter(a)
# print(next(it))
# print(next(it))
# print(next(it))

# b = EvenNumberIterator(10)
# for i in b:
#     print(i)
a = EvenNumbers()
b = iter(a)
print(next(b))
print(next(b))
print(next(b))
# print(list(islice(b, 3, 10, 2)))
print(list(islice(b, 3)))
print(list(islice(b, 3)))