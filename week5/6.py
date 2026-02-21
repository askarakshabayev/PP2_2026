import math
from itertools import islice

class PrimeNumber:
    def __init__(self):
        self.current = 2

    def next_prime(self):
        value = self.current
        value += 1 
        found = False # found = False
        while not found:
            found = True # found = True
            for i in range(2, int(math.sqrt(value)) + 1):
                if value % i == 0:
                    found = False
                    break
            if not found:
                value += 1 
        return value

    def __iter__(self):
        return self

    def __next__(self):
        value = self.current # value = 5
        self.current = self.next_prime() # 7
        return value

a = PrimeNumber()
it = iter(a)
# print(next(it))
# print(next(it))
# print(next(it))
# print(next(it))
        
print(list(islice(it, 2, 10, 2)))