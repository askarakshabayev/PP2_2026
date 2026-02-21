def inner():
    yield 1
    yield 2
    yield 3

def outer():
    yield "start" 
    yield from inner()
    yield "end"

print(list(outer()))

# start
# 1
# 2
# 3
# end
