import math

class PrimeNumber:
    def __init__(self, end):
        self.current = 2
        self.end = end

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
        if value > self.end:
            raise StopIteration
        self.current = self.next_prime() # 7
        return value

a = PrimeNumber(1000)
# it = iter(a)
# print(next(it))
# print(next(it))
# print(next(it))
# print(next(it))
        
for i in a:
    # if i > 1000:
    #     break
    print(i)