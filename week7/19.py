import os


# for name in os.listdir():
#     if os.path.isfile(name):
#         print("FILE:", name)
#     else:
#         print("DIR:", name)

base = os.getcwd()

def func(url, level = 0): # /Users/askar/pp2_2026/week7
    intend = "   " * level
    for name in os.listdir(url): # 1.py
        url_check = os.path.join(url, name) # /Users/askar/pp2_2026/week7/1.py
        if os.path.isfile(url_check):
            print(intend, name)
        else:
            print(intend, name)
            func(url_check, level + 1)

func(base)

# hello
#     a
#         b
#             c
# week7_test
#     week_test_2
#         a.py
#     test.py
# 1.py
# 2.py
