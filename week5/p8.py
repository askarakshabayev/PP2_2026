# def gen_squares(n):
#     l = []
#     for i in range(n):
#         l.append(i ** 2)
#     return l

# a = gen_squares(5)
# print(a)

# def gen_squares_generator(n):
#     for i in range(n):
#         yield i ** 2

# b = list(gen_squares_generator(5))
# print(b)

squares_list = [x ** 2 for x in range(10)]
squares_gen = (x ** 2 for x in range(10))

print(sum(squares_list))
print(sum(squares_gen))