f = open("input.txt", "r")

# Example 1
# text = f.read()
# print(text)

# Example 2
# line1 = f.readline()
# line2 = f.readline()

# print(line1)
# print(line2)

# Example 3
# lines = f.readlines()
# print(lines)

# Example 4
for line in f:
    print(line)
f.close()