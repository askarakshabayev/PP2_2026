def read_lines(filename):
    with open(filename, 'r') as f:
        for line in f:
            yield line.strip() # 2

for line in read_lines("a.txt"):
    print(line)
