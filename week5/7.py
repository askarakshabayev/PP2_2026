import random

random.seed(100)

rolls = iter(lambda: random.randint(1, 6), 6)

print(list(rolls))