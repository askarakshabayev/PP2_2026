words = ["banana", 'ccc', "kiwi", 'bbb', "apple", "fig", 'aaa']

sorted_ws = sorted(words, key=lambda x: (len(x), x))
# (6, "banana")
# (3, "ccc") <-
# (4, "kiwi")
# (3, "bbb") 
# (5, "apple")
# (3, "fig")  
# (3, "aaa") <-


print(sorted_ws)