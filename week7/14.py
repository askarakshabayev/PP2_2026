a = ("Aaa", "Bbb", "Ccc", "Dddd")
b = (90, 65, 76, 80)

zipped = list(zip(a, b))
print(list(filter(lambda x: x[1] >= 80, zipped)))