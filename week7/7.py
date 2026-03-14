a = ["Aaa", "Bbb", "Ccc", "Ddd"]
b = [95, 60, 72, 85]

c = list(zip(a, b))
q, w = zip(*c)
print(q)
print(w)

# q = a 
# w = b