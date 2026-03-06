from datetime import datetime, date

now = datetime.now()


print(now.year)
print(now.month)
print(now.day)
print(now.hour)

today = date.today()

print(today)

quiz_2 = date(2026, 3, 15)
print(quiz_2)