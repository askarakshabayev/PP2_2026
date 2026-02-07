a = {"abc", "def", 1, 2, 3}

try:
    a.remove(10)
except Exception as e:
    # print("Error", str(e))
    pass

print(a)

