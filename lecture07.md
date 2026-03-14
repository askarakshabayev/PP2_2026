# Lecture 7: Built-ins & Work with Files

## Plan
- Built-in Python functions overview (`map`, `filter`, `enumerate`, `zip`, `sorted`, `any`, `all`, etc.)
- File handling: reading (`r`), writing (`w`), appending (`a`)
- Working with directories (`os`)
- Creating and deleting files and directories

---

## 1. Useful Built-in Functions

Python ships with many powerful built-in functions. No imports needed.

### `map()` — apply a function to every element

```python
# map(function, iterable) → returns a map object (lazy)
numbers = [1, 2, 3, 4, 5]

doubled = list(map(lambda x: x * 2, numbers))
print(doubled)  # [2, 4, 6, 8, 10]

# Works with any function
words = ["hello", "world", "python"]
upper = list(map(str.upper, words))
print(upper)  # ['HELLO', 'WORLD', 'PYTHON']
```

### `filter()` — keep only elements that match a condition

```python
# filter(function, iterable) → returns a filter object (lazy)
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

evens = list(filter(lambda x: x % 2 == 0, numbers))
print(evens)  # [2, 4, 6, 8, 10]

words = ["apple", "banana", "kiwi", "cherry", "fig"]
long_words = list(filter(lambda w: len(w) > 4, words))
print(long_words)  # ['apple', 'banana', 'cherry']
```

### `enumerate()` — iterate with index

```python
# enumerate(iterable, start=0) → yields (index, value) pairs
fruits = ["apple", "banana", "cherry"]

for i, fruit in enumerate(fruits):
    print(f"{i}: {fruit}")
# 0: apple
# 1: banana
# 2: cherry

# Start index from 1
for i, fruit in enumerate(fruits, start=1):
    print(f"{i}. {fruit}")
# 1. apple
# 2. banana
# 3. cherry
```

### `zip()` — pair elements from multiple iterables

```python
# zip(iter1, iter2, ...) → stops at the shortest iterable
names = ["Alice", "Bob", "Charlie"]
scores = [95, 80, 72]

for name, score in zip(names, scores):
    print(f"{name}: {score}")
# Alice: 95
# Bob: 80
# Charlie: 72

# Convert to list of tuples
pairs = list(zip(names, scores))
print(pairs)  # [('Alice', 95), ('Bob', 80), ('Charlie', 72)]

# Unzip (reverse of zip)
n, s = zip(*pairs)
print(list(n))  # ['Alice', 'Bob', 'Charlie']
print(list(s))  # [95, 80, 72]
```

### `sorted()` and `reversed()`

```python
nums = [3, 1, 4, 1, 5, 9, 2, 6]

print(sorted(nums))              # [1, 1, 2, 3, 4, 5, 6, 9]
print(sorted(nums, reverse=True))# [9, 6, 5, 4, 3, 2, 1, 1]

# Sort by key
words = ["banana", "kiwi", "apple", "fig"]
print(sorted(words, key=len))    # ['fig', 'kiwi', 'apple', 'banana']

# reversed() — lazy iterator
for x in reversed([1, 2, 3]):
    print(x, end=' ')  # 3 2 1
```

### `any()` and `all()`

```python
nums = [2, 4, 6, 7, 10]

print(any(x % 2 != 0 for x in nums))   # True  (7 is odd)
print(all(x % 2 == 0 for x in nums))   # False (7 is odd)

passwords = ["abc123", "qwerty", "Pass1word"]
print(any(len(p) >= 8 for p in passwords))  # True
print(all(len(p) >= 8 for p in passwords))  # False
```

### Other useful builtins

```python
# min / max with key
words = ["banana", "kiwi", "apple"]
print(min(words, key=len))   # kiwi
print(max(words, key=len))   # banana

# sum
print(sum([1, 2, 3, 4, 5]))         # 15
print(sum([1, 2, 3], start=10))     # 16  (Python 3.8+: start param)

# abs, round, pow
print(abs(-42))       # 42
print(round(3.14159, 2))  # 3.14
print(pow(2, 10))     # 1024

# len, type, isinstance
print(len("hello"))           # 5
print(type(3.14))             # <class 'float'>
print(isinstance(42, int))    # True
```

### Task 1

Given a list of student names and their grades, use `zip`, `filter`, and `map` to print only the names of students who passed (grade >= 60), converted to uppercase.


**Solution:**

```python
names  = ["Alice", "Bob", "Charlie", "Diana", "Eve"]
grades = [85, 55, 72, 48, 91]

passed = [(name, grade) for name, grade in zip(names, grades) if grade >= 60]
result = list(map(lambda pair: pair[0].upper(), passed))

print(result)  # ['ALICE', 'CHARLIE', 'EVE']
```

### Task 2

You have a list of prices (floats). Use `enumerate` to print each item with its 1-based index, then use `filter` to find all items over 1000, and print the total using `sum`.

**Solution:**

```python
prices = [499.99, 1200.00, 350.50, 2500.00, 899.99, 1050.00]

for i, price in enumerate(prices, start=1):
    print(f"  {i}. {price:.2f}")

expensive = list(filter(lambda p: p > 1000, prices))
print(f"Expensive items: {expensive}")
print(f"Total: {sum(expensive):.2f}")
# Expensive items: [1200.0, 2500.0, 1050.0]
# Total: 4750.00
```

---

## 2. File Handling

### Opening a file — `open(path, mode)`

| Mode | Meaning |
|------|---------|
| `'r'` | Read (default). Error if file doesn't exist |
| `'w'` | Write. Creates file or **overwrites** existing |
| `'a'` | Append. Creates file or adds to the end |
| `'x'` | Create. Error if file already exists |

### Reading a file

```python
# Method 1: read entire content at once
f = open('input.txt', 'r')
content = f.read()
print(content)
f.close()

# Method 2: read line by line
f = open('input.txt', 'r')
line1 = f.readline()
line2 = f.readline()
print(line1, line2)
f.close()

# Method 3: read all lines into a list
f = open('input.txt', 'r')
lines = f.readlines()   # ['line1\n', 'line2\n', ...]
print(lines)
f.close()

# Method 4: iterate (most memory-efficient)
f = open('input.txt', 'r')
for line in f:
    print(line.strip())
f.close()
```

### Using `with` — the right way

The `with` statement automatically closes the file even if an error occurs.

```python
with open('input.txt', 'r') as f:
    for line in f:
        print(line.strip())
# file is closed here automatically
```

### Writing and Appending

```python
# Write mode — creates or overwrites
with open('output.txt', 'w') as f:
    f.write('Hello World\n')
    f.write('Second line\n')

# Append mode — adds to the end
with open('output.txt', 'a') as f:
    f.write('Appended line\n')

# Create mode — fails if file already exists
with open('new_file.txt', 'x') as f:
    f.write('Brand new file\n')
```

### Task 3

Write a program that reads `input.txt` line by line, strips whitespace from each line, and writes the result to `output.txt` (one line per line). Then append a final line `"--- end of file ---"`.

**Solution:**

```python
with open('input.txt', 'r') as f_in:
    lines = [line.strip() for line in f_in if line.strip()]

with open('output.txt', 'w') as f_out:
    for line in lines:
        f_out.write(line + '\n')

with open('output.txt', 'a') as f_out:
    f_out.write('--- end of file ---\n')
```

### Task 4

Read a file of numbers (one per line), compute the sum and average, and write the results to `result.txt`.

**Solution:**

```python
with open('numbers.txt', 'r') as f:
    numbers = [int(line.strip()) for line in f if line.strip()]

total   = sum(numbers)
average = total / len(numbers)

with open('result.txt', 'w') as f:
    f.write(f"Count:   {len(numbers)}\n")
    f.write(f"Sum:     {total}\n")
    f.write(f"Average: {average:.2f}\n")
```

---

## 3. Working with Directories (`os`)

```python
import os
```

### Current directory and navigation

```python
import os

print(os.getcwd())          # /Users/askar/Documents/KBTU/PP2_2026
os.chdir('week7')           # change into a subdirectory
print(os.getcwd())          # /Users/askar/Documents/KBTU/PP2_2026/week7
```

### Checking paths

```python
import os

path = 'input.txt'

os.path.exists(path)    # True/False — path exists at all?
os.path.isfile(path)    # True/False — is it a file?
os.path.isdir(path)     # True/False — is it a directory?
os.path.join('dir1', 'dir2', 'file.txt')  # 'dir1/dir2/file.txt'
```

### Listing contents — `os.listdir`

```python
import os

BASE = os.getcwd()

for name in os.listdir(BASE):
    full_path = os.path.join(BASE, name)
    if os.path.isfile(full_path):
        print(f'FILE: {name}')
    else:
        print(f' DIR: {name}')
```

### Walking the entire tree — `os.walk`

`os.walk` yields `(root, dirs, files)` for each directory recursively.

```python
import os

for root, dirs, files in os.walk(os.getcwd()):
    print(f"In: {root}")
    for d in dirs:
        print(f"  DIR:  {d}")
    for f in files:
        print(f"  FILE: {f}")
```

### Scanning — `os.scandir`

More efficient than `os.listdir` — gives `DirEntry` objects with metadata.

```python
import os

with os.scandir('.') as entries:
    for entry in entries:
        if entry.is_file():
            print(f'File: {entry.name}')
        elif entry.is_dir():
            print(f'Dir:  {entry.name}')
```

### Task 5

Write a function `find_files(directory, extension)` that returns a list of all files with the given extension inside the directory (not recursive).

**Solution:**

```python
import os

def find_files(directory, extension):
    result = []
    with os.scandir(directory) as entries:
        for entry in entries:
            if entry.is_file() and entry.name.endswith(extension):
                result.append(entry.name)
    return result

py_files = find_files('.', '.py')
print(py_files)
```

### Task 6

Write a recursive function `show_tree(path, level=0)` that prints the directory tree with indentation.

**Solution:**

```python
import os

def show_tree(path, level=0):
    indent = '  ' * level
    for name in os.listdir(path):
        full = os.path.join(path, name)
        if os.path.isfile(full):
            print(f'{indent}FILE: {name}')
        else:
            print(f'{indent}DIR:  {name}')
            show_tree(full, level + 1)

show_tree(os.getcwd())
```

---

## 4. Creating and Deleting Files & Directories

### Creating

```python
import os

os.mkdir('new_folder')              # create single directory
os.makedirs('a/b/c/d', exist_ok=True)  # create nested dirs, no error if exists
```

### Renaming

```python
import os

os.rename('old_name.txt', 'new_name.txt')   # rename file or directory
```

### Deleting files and directories

```python
import os
import shutil

os.remove('file.txt')       # delete a file
os.rmdir('empty_dir')       # delete an empty directory
shutil.rmtree('full_dir')   # delete a directory and ALL its contents
```

### Copying and moving

```python
import shutil

shutil.copy('file.txt', 'backup/file.txt')      # copy a file
shutil.copytree('dir1', 'dir1_backup')          # copy entire directory
shutil.move('file.txt', 'archive/')             # move file or directory
```

### Safe utility functions

Always check before operating to avoid errors:

```python
import os
import shutil

def safe_remove(path):
    if os.path.isfile(path):
        os.remove(path)
        print(f'Deleted file: {path}')
    else:
        print(f'File not found: {path}')

def safe_rmdir(path):
    if os.path.isdir(path):
        shutil.rmtree(path)
        print(f'Deleted directory: {path}')
    else:
        print(f'Directory not found: {path}')

def create_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)
        print(f'Created: {path}')
    else:
        print(f'Already exists: {path}')
```

### Task 7

Write a program that:
1. Creates a directory `archive/`
2. Creates 3 text files inside it: `log1.txt`, `log2.txt`, `log3.txt` with some content
3. Lists all files in `archive/`
4. Deletes `log2.txt`
5. Lists the directory again

**Solution:**

```python
import os

# 1. Create directory
os.makedirs('archive', exist_ok=True)

# 2. Create files
for i in range(1, 4):
    with open(f'archive/log{i}.txt', 'w') as f:
        f.write(f'Log entry #{i}\n')

# 3. List
print("Before:", os.listdir('archive'))

# 4. Delete log2.txt
os.remove('archive/log2.txt')

# 5. List again
print("After: ", os.listdir('archive'))
```

### Task 8

Write a program that scans the current directory and **copies** all `.py` files into a new folder called `py_backup/`.

**Solution:**

```python
import os
import shutil

os.makedirs('py_backup', exist_ok=True)

with os.scandir('.') as entries:
    for entry in entries:
        if entry.is_file() and entry.name.endswith('.py'):
            shutil.copy(entry.path, os.path.join('py_backup', entry.name))
            print(f'Copied: {entry.name}')
```

---

## Conclusion

### Key Takeaways

**Useful Built-ins:**
- `map(fn, iterable)` — apply a function to every element, returns lazy iterator
- `filter(fn, iterable)` — keep elements where `fn(x)` is True
- `enumerate(iterable, start=0)` — adds an index counter to iteration
- `zip(a, b)` — pairs elements from multiple iterables; stops at shortest
- `sorted(iterable, key=fn, reverse=False)` — returns a new sorted list
- `any(iterable)` / `all(iterable)` — at least one / all elements are truthy
- `min`, `max` accept a `key=` function; `sum`, `abs`, `round` for math

**File Handling:**
- `open(path, mode)` — `'r'` read, `'w'` write/overwrite, `'a'` append, `'x'` create
- Always use `with open(...) as f:` — file closes automatically
- `f.read()`, `f.readline()`, `f.readlines()`, iterating `for line in f`
- `f.write(text)` — writes a string (add `\n` manually for newlines)

**Working with Directories (`os`):**
- `os.getcwd()` / `os.chdir(path)` — get/change current directory
- `os.path.exists()`, `os.path.isfile()`, `os.path.isdir()` — path checks
- `os.path.join(a, b)` — safely combine path parts (cross-platform)
- `os.listdir(path)` — list names; `os.scandir(path)` — list with metadata
- `os.walk(path)` — recursive `(root, dirs, files)` generator

**Creating and Deleting:**
- `os.mkdir(path)` — one directory; `os.makedirs(path, exist_ok=True)` — nested
- `os.rename(old, new)` — rename file or directory
- `os.remove(path)` — delete file; `os.rmdir(path)` — delete empty dir
- `shutil.rmtree(path)` — delete dir with all contents
- `shutil.copy(src, dst)`, `shutil.copytree(src, dst)`, `shutil.move(src, dst)`

**`pathlib` (modern alternative):**
- `Path('.')` — create a Path object; `/` operator builds sub-paths
- `.read_text()` / `.write_text()` — file I/O without `open()`
- `.iterdir()` — list directory; `.rglob('*.py')` — recursive pattern search
