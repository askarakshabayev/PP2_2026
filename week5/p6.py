import random

l = iter(lambda: random.randint(1, 6), 6)
print(list(l))