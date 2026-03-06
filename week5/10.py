def gen_squares_list(n):
    result = []
    for i in range(n):
        result.append(i ** 2)
    return result

def get_squares_gen(n):
    for i in range(n): # i = 1
        yield i ** 2   # i * i

print(list(gen_squares_list(5)))
print(list(get_squares_gen(5)))