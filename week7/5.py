words = ["apple", "banana", "abc", "tt", "testtest"]

f_w = list(filter(lambda x: len(x) > 4, words))

print(f_w)