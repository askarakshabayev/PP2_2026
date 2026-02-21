def inner():
    yield 1
    yield 2
    yield 3

def outer():
    yield "start"
    yield from inner()
    yield "stop"

print(list(outer()))