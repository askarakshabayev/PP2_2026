import os
import shutil

def my_print(indent):
    for i in range(indent):
        print("   ", end = '')

def show_tree(url, indent = 0):
    ind = "  " * indent
    for dir_entry in os.scandir(url):
        if dir_entry.is_dir():
            print(ind + dir_entry.name)
            show_tree(os.path.join(url, dir_entry.name), indent + 1)
        else:
            my_print(indent)
            print(ind + dir_entry.name)


base = os.getcwd()
# show_tree(base)
# print(os.walk(os.getcwd()))

# for dir_entry in os.scandir(base):
#     print(dir_entry.)

# os.mkdir("hello")
# os.makedirs("hello/a/b/c", exist_ok=True)
shutil.copy("p1.py", "p2.py")
shutil.copytree("week7_test", "week7_test_v2")