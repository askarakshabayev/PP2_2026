from datetime import datetime, date
def calculate_age(birthday):
    now = datetime.now()
    age = now.year - birthday.year
    return age

b = date(1986, 2, 13)
print(calculate_age(b))
