# import math
# from math import pi, sqrt
# print(math.pi)
# print(math.sqrt(16))

# from mymath import sum, multiply

# a = sum(3, 4)
# b = multiply(2, 4)
# print(a, b)

from datetime import datetime, date, time, timedelta

now = datetime.now()
# print(now.date())
# print(now.time())
# print(now.year)

# d = date(2026, 2, 10)
# print(d)
# d1 = d + timedelta(days=2)
# print(d1)

print(now.strftime("year = %Y, month = %m"))