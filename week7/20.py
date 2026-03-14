import os

a = os.walk(os.getcwd())
# root, dirs, files = next(a)
# root, dirs, files = next(a)
# root, dirs, files = next(a)
# root, dirs, files = next(a)
# print(root)
# print(dirs)
# print(files)
for root, dirs, files in os.walk(os.getcwd()):
    print(f"In: {root}")
    for d in dirs:
        print(f"  DIR:  {d}")
    for f in files:
        print(f"  FILE: {f}")
