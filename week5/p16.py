import random
import string

def gen_password(l=10):
    a = string.ascii_letters + string.digits
    password = ''.join(random.choices(a, k=l))
    return password

def roll_dice(num_dice=2, sides=6):
    rolls = [random.randint(1, sides) for _ in range(num_dice)]
    return rolls, sum(rolls)

# p = gen_password(10)
# print(p)

p = roll_dice()
print(p)