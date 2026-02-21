l = [5, 1, 8, 10, 12] 
# __iter__ 
# __next__

# for i in l:
#     print(i)

# it = iter(l)
# print(next(it))
# print(next(it))
# print(next(it))
# print(next(it))
# print(next(it))
# print(next(it))

# for i in l:
#     for j in l:
#         print(i, j)

it = iter(l)

for i in it: # i = 5
    for j in it: # j = 8
        print(i, j) 

# 5 1 
# 5 8
# 5 10
# 5 12



