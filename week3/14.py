def my_sum(*args):
    result = 0
    for x in args:
        result += x
    return result

a = my_sum(1, 2, 3)
b = my_sum(1, 2, 3, 4, 5)
print(a)
print(b)