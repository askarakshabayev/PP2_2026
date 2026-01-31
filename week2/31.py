# a = []
# for i in range(20):
#     if i % 2 == 0:
#         a.append(i)

a = [i * i for i in range(20) if i % 2 == 0]
print(a)