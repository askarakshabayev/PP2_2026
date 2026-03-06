# import random
# import string

# def gen_password(len=6):
#     characters = string.ascii_letters + string.digits
#     print(characters)
#     password = ''.join(random.choices(characters, k=len))
#     return password

# pass1 = gen_password(10)
# pass2 = gen_password(12)
# pass3 = gen_password()

# print(pass1)
# print(pass2)
# print(pass3)

import random
def roll_dice(num_dice = 2, sides = 6):
    rolls = [random.randint(1, sides) for _ in range(num_dice)]
    return rolls, sum(rolls)

print(roll_dice(num_dice=3))
