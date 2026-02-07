fib = dict()
def rec(n):
    if n in fib:
        return fib[n]

    if n == 0 or n == 1:
        return 1
    
    fib[n] = rec(n - 1) + rec(n - 2)
    return fib[n]

print(rec(5))