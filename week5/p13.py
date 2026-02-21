x = 10

def broken():
    print(x)  # UnboundLocalError! Python sees the assignment below
    x = 20    # and treats x as local for the entire function

# broken()