# Lecture 2: Control Flow, Collections & Iteration

## Topics Covered
- Input/Output Operations
- Operators (Bitwise, Logical)
- While Loops
- For Loops
- Lists: Indexing, Slicing, Methods
- Tuples
- Sets
- Dictionaries
- Iteration over Collections
- List Comprehensions

---

## 1. Input and Output Operations

### Basic Input and Addition

**Example 1: Simple Input**
```python
a = int(input())
b = int(input())

print(a + b)
```

**Example 2: Using split() for Multiple Inputs**
```python
# Input: 2 3
a, b = input().split()

print(int(a) + int(b))
```

**Example 3: Using map() for Type Conversion**
```python
a, b = map(int, input().split())
print(a + b)
```

**Example 4: map() Returns an Iterator**
```python
a = map(int, input().split())

# print(a)  # This would show a map object

for x in a:
    print(x, end=' ')
```

---

## 2. Operators

### Bitwise Operators

Bitwise operators work at the binary level and are useful for performance-critical operations.

**Example 5: Bit Shifting**
```python
a = 2
# a += 10  # a = a + 10

# Left shift: multiply by 2^n
a <<= 3  # a = a << 3

print(a)  # 16

# 2 -> 10 (binary)
# 2 << 3 => 10000 (binary) => 16 (decimal)

a = 5
# Right shift: divide by 2^n
a >>= 1
print(a)  # 2

# 5 -> 101 (binary)
# 5 >> 1 => 10 (binary) -> 2 (decimal)
```

**Example 6: Bitwise AND, OR, XOR**
```python
a = 5  # 101
b = 3  # 011
       # 011 => 3

a &= b  # Bitwise AND

# AND Truth Table:
# 1 & 1 = 1
# 1 & 0 = 0
# 0 & 1 = 0
# 0 & 0 = 0

# 5 = 101
# 3 = 011
#     001 => 1

print(a)  # 1
```

### Logical Operators

**Example 7: Boolean Logic**
```python
a = 5
b = 6
c = 7
print(not (a > b and a > c))  # True

# a > b is False
# a > c is False
# False and False = False
# not False = True
```

---

## 3. Conditional Statements

**Example 8: Finding Maximum of Three Numbers**
```python
a, b, c = map(int, input().split())

# Comparison operators:
# a == b  (equal)
# a != b  (not equal)
# a < b   (less than)
# a <= b  (less than or equal)
# a > b   (greater than)
# a >= b  (greater than or equal)

if a >= b and a >= c:
    print(a)
elif b >= a and b >= c:
    print(b)
else:
    print(c)
```

---

## 4. While Loops

While loops continue executing as long as a condition is True.

**Example 9: While Loop with break and continue**
```python
i = 0

# Example with break
# while i < 10:
#     i += 1
#     print(i)
#     if i == 5:
#         break  # Exit loop when i equals 5

# Example with continue
while i < 10:
    i += 1
    if i % 2 == 0:
        continue  # Skip even numbers
    print(i)
else:
    print("end")  # Executes when loop completes normally
```

**Key Points:**
- `break`: Exit the loop immediately
- `continue`: Skip to the next iteration
- `else`: Executes when loop completes without break

---

## 5. For Loops

For loops iterate over sequences (lists, ranges, strings, etc.).

**Example 10: Iterating Over a List**
```python
a = [12, 3, 8, 10, 13]

for x in a:
    print(x)
```

**Example 11: Using range()**
```python
# range(start, stop, step)
for x in range(1, 20, 5):
    print(x)  # Prints: 1, 6, 11, 16
```

**Example 12: Nested For Loops**
```python
a = [1, 2, 3]
b = [3, 4, 5]

for x in a:
    for y in b:
        print(x, y)
```

**Example 13: Iterating with Indices**
```python
a = [12, 5, 6, 10]

for i in range(len(a)):  # 0 to len(a)-1
    print(a[i])
```

**Example 13a: Looping Through Strings**
```python
# You can iterate through any sequence, including strings
for x in "banana":
    print(x)  # Prints each character: b, a, n, a, n, a
```

**Example 13b: Range with Different Parameters**
```python
# range(start, stop)
for x in range(2, 6):
    print(x)  # 2, 3, 4, 5

# range(start, stop, step)
for x in range(2, 30, 3):
    print(x)  # 2, 5, 8, 11, 14, 17, 20, 23, 26, 29

# Counting backwards
for x in range(10, 0, -1):
    print(x)  # 10, 9, 8, 7, 6, 5, 4, 3, 2, 1
```

**Example 13c: Pass Statement**
```python
# Use pass when you need a loop with no content yet
for x in [0, 1, 2]:
    pass  # Placeholder for future code
# This prevents syntax errors when defining empty loops
```

---

## 6. Lists

Lists are ordered, mutable collections that can hold items of different types.

### List Basics and Indexing

**Example 14: List Types and Nested Lists**
```python
list1 = ["apple", "banana", "cherry"]
list2 = [1, 5, 10, 20]
list3 = [True, False, False]
list4 = ["abc", 34, True, 40, "name", [1, 2, 3]]

print(list4[5][2])  # Accessing nested list: 3
```

### Indexing and Slicing

**Example 14a: Negative Indexing**
```python
thislist = ["apple", "banana", "cherry", "orange", "kiwi"]

# Negative indexing starts from the end
print(thislist[-1])  # kiwi (last item)
print(thislist[-2])  # orange (second from end)
print(thislist[-3])  # cherry
```

**Example 14b: Advanced Slicing**
```python
thislist = ["apple", "banana", "cherry", "orange", "kiwi", "melon", "mango"]

# Slicing with step
print(thislist[::2])    # ['apple', 'cherry', 'kiwi', 'mango'] (every 2nd item)
print(thislist[1::2])   # ['banana', 'orange', 'melon'] (start at index 1, every 2nd)
print(thislist[::-1])   # Reverse the list
print(thislist[1:5:2])  # ['banana', 'orange'] (from index 1 to 5, step 2)
```

**Example 14c: Changing Range of Items**
```python
thislist = ["apple", "banana", "cherry", "orange", "kiwi", "mango"]

# Replace multiple items with slicing
thislist[1:3] = ["blackcurrant", "watermelon"]
print(thislist)  # ['apple', 'blackcurrant', 'watermelon', 'orange', 'kiwi', 'mango']

# Replace with more items
thislist[1:2] = ["grape", "strawberry"]
print(thislist)  # ['apple', 'grape', 'strawberry', 'watermelon', 'orange', 'kiwi', 'mango']
```

**Example 14d: Membership Testing**
```python
thislist = ["apple", "banana", "cherry"]

# Check if item exists
if "apple" in thislist:
    print("Yes, 'apple' is in the list")

if "orange" not in thislist:
    print("No, 'orange' is not in the list")
```

### List Methods

**Example 15: append(), pop(), clear()**
```python
a = []

# append(): Add elements to the end
for x in range(0, 20, 2):
    a.append(x)

# pop(): Remove element at index
a.pop(1)  # Remove element at index 1
a.pop(5)  # Remove element at index 5

# clear(): Remove all elements
a.clear()
print(a)  # []
```

**Example 16: count()**
```python
a = [1, 2, 3, 1, 2, 3, 1, 2, 3]
a = [1, "abc", "2", "1", "hello", 2, "1"]

x = a.count("1")  # Count occurrences of "1"
print(x)  # 3
```

**Example 17: List Multiplication**
```python
a = [0, 1, 2, 3, 4, 5] * 5
print(a)  # [0, 1, 2, 3, 4, 5, 0, 1, 2, 3, 4, 5, ...]
```

**Example 18: extend(), insert(), remove(), index()**
```python
a = [1, 2, 3]
b = [5, 6, 7]

# extend(): Add all elements from another list
a.extend(b)

# insert(): Add element at specific index
a.insert(1, "hello")  # Insert "hello" at index 1
a.insert(4, "hello")  # Insert "hello" at index 4

# remove(): Remove first occurrence of value
a.remove("hello")  # Removes first "hello"

# index(): Find index of element
# p = a.index(6)
# print(p)

print(a)
```

**Example 19: sort(), reverse()**
```python
a = [12, 1, 45, 16, 57]

# sort(): Sort list in ascending order
# a.sort()

# reverse(): Reverse the list
a.reverse()
print(a)  # [57, 16, 45, 1, 12]
```

### List References and Copying

**Example 20: References**
```python
a = [1, 2, 3]  # a points to list [1, 2, 3]
b = a          # b points to the SAME list

a.append(4)
b.append(5)

print(hex(id(a)))  # Same memory address
print(hex(id(b)))  # Same memory address

# Both a and b refer to [1, 2, 3, 4, 5]
```

**Example 21: Copying Lists**
```python
a = [1, 2, 3]
b = a.copy()  # Create a separate copy

a.append(4)
b.append(5)

print(a)  # [1, 2, 3, 4]
print(b)  # [1, 2, 3, 5]

print(hex(id(a)))  # Different memory address
print(hex(id(b)))  # Different memory address
```

**Example 21a: List Concatenation**
```python
list1 = ["a", "b", "c"]
list2 = [1, 2, 3]

# Using + operator
list3 = list1 + list2
print(list3)  # ['a', 'b', 'c', 1, 2, 3]

# Using extend() - modifies list1
list1.extend(list2)
print(list1)  # ['a', 'b', 'c', 1, 2, 3]
```

---

## 7. Tuples

Tuples are ordered, **immutable** collections. Once created, they cannot be modified.

**Example 22: Tuple Basics**
```python
# Creating a tuple
a = (1, 2, 3, 1)

print(a.count(1))  # Count occurrences: 2

# Iterating over tuple
for x in a:
    print(x)

# Tuples are immutable
# a[0] = 5  # This would raise an error!
```

**Example 22a: Single-Item Tuple (Requires Comma!)**
```python
# Correct: This is a tuple
thistuple = ("apple",)  # Note the comma!
print(type(thistuple))  # <class 'tuple'>

# Wrong: This is NOT a tuple, it's a string
thistuple = ("apple")
print(type(thistuple))  # <class 'str'>
```

**Example 22b: Tuple Indexing and Slicing**
```python
thistuple = ("apple", "banana", "cherry", "orange", "kiwi", "melon", "mango")

# Positive indexing
print(thistuple[1])   # banana
print(thistuple[2])   # cherry

# Negative indexing
print(thistuple[-1])  # mango
print(thistuple[-2])  # melon

# Slicing
print(thistuple[2:5])   # ('cherry', 'orange', 'kiwi')
print(thistuple[-4:-1]) # ('orange', 'kiwi', 'melon')
print(thistuple[:3])    # ('apple', 'banana', 'cherry')
```

**Example 22c: Tuple Unpacking**
```python
fruits = ("apple", "banana", "cherry")

# Unpacking into variables
(green, yellow, red) = fruits

print(green)   # apple
print(yellow)  # banana
print(red)     # cherry

# Unpacking with * (asterisk)
fruits = ("apple", "banana", "cherry", "strawberry", "raspberry")
(green, yellow, *red) = fruits

print(green)   # apple
print(yellow)  # banana
print(red)     # ['cherry', 'strawberry', 'raspberry'] (list!)
```

**Example 22d: Tuple Concatenation and Multiplication**
```python
# Concatenation
tuple1 = ("a", "b", "c")
tuple2 = (1, 2, 3)
tuple3 = tuple1 + tuple2
print(tuple3)  # ('a', 'b', 'c', 1, 2, 3)

# Multiplication
fruits = ("apple", "banana", "cherry")
mytuple = fruits * 2
print(mytuple)  # ('apple', 'banana', 'cherry', 'apple', 'banana', 'cherry')
```

**When to Use Tuples:**
- Data that shouldn't change (coordinates, RGB colors, etc.)
- Dictionary keys (lists can't be keys)
- Returning multiple values from functions
- Slightly faster than lists

---

## 8. List Comprehensions

List comprehensions provide a concise way to create lists.

**Example 23: Basic List Comprehension**
```python
# Traditional way
# for i in range(5):
#     print(i)

# List comprehension with condition
a = [i for i in range(10) if i % 2 == 0]
print(a)  # [0, 2, 4, 6, 8]
```

**Example 24: List Comprehension with Input**
```python
# Input: 1 2 3.3
a = [float(n) for n in input().split()]
b = [a[i] ** 2 for i in range(len(a))]

print(a)  # [1.0, 2.0, 3.3]
print(b)  # [1.0, 4.0, 10.89]
```

**Example 25: Combining Two Lists**
```python
a = [1, 2, 3]
b = [4, 5, 6]

# Element-wise multiplication
c = [a[i] * b[i] for i in range(len(a))]

# Equivalent to:
# c = []
# for i in range(len(a)):
#     c.append(a[i] * b[i])

print(c)  # [4, 10, 18]
```

**Example 25a: List Comprehension with String Manipulation**
```python
fruits = ["apple", "banana", "cherry"]

# Convert to uppercase
newlist = [x.upper() for x in fruits]
print(newlist)  # ['APPLE', 'BANANA', 'CHERRY']

# Get lengths
lengths = [len(x) for x in fruits]
print(lengths)  # [5, 6, 6]
```

**Example 25b: List Comprehension with if-else (Ternary Operator)**
```python
fruits = ["apple", "banana", "cherry", "kiwi", "mango"]

# Replace 'banana' with 'orange', keep others
newlist = [x if x != "banana" else "orange" for x in fruits]
print(newlist)  # ['apple', 'orange', 'cherry', 'kiwi', 'mango']

# Set all values to same
newlist = ['hello' for x in fruits]
print(newlist)  # ['hello', 'hello', 'hello', 'hello', 'hello']
```

**Example 25c: Advanced List Comprehension**
```python
# Filter and transform
fruits = ["apple", "banana", "cherry", "kiwi", "mango"]
newlist = [x.upper() for x in fruits if "a" in x]
print(newlist)  # ['APPLE', 'BANANA', 'MANGO']

# Nested list comprehension - creating multiplication table
matrix = [[i * j for j in range(1, 4)] for i in range(1, 4)]
print(matrix)  # [[1, 2, 3], [2, 4, 6], [3, 6, 9]]
```

---

## 9. Sets

Sets are unordered collections of **unique** elements.

**Example 26: Set Basics**
```python
# Creating a set
a = set()
a.add(1)
a.add(2)
a.add(1)  # Duplicate, won't be added
a.add(3)

# Iterating over set
# for x in a:
#     print(x)

# Membership testing
if 4 in a:
    print("YES")
else:
    print("NO")  # This will print
```

**Example 27: Set remove() with Exception Handling**
```python
set1 = set()
set1.add(1)
set1.add(2)
set1.add(3)

try:
    set1.remove(10)  # Raises error if element doesn't exist
except Exception as e:
    print("Error: " + str(e))

print(set1)
print("hello world")

# Alternative: use discard() which doesn't raise error
# set1.discard(10)  # Safe removal
```

**Example 28: Set Operations**
```python
set1 = set([1, 2, 3, 5])
set2 = set([2, 3, 4])
set3 = set([3, 4, 5, 6])

# Union: all unique elements
# print(set1.union(set2, set3))  # {1, 2, 3, 4, 5, 6}

# Union with list
# print(set1.union([10, 20, 1, 2]))  # {1, 2, 3, 5, 10, 20}

# Intersection: common elements
# print(set1.intersection(set2, set3))  # {3}

# Difference: elements in set1 but not in others
# print(set1.difference(set2))  # {1, 5}

# Using operators
print(set1 - set2 - set3)  # {1}
```

**Example 28a: discard() vs remove()**
```python
thisset = {"apple", "banana", "cherry"}

# remove() raises error if item doesn't exist
try:
    thisset.remove("orange")
except KeyError:
    print("'orange' not found!")

# discard() does NOT raise error if item doesn't exist
thisset.discard("orange")  # No error - safe to use
thisset.discard("banana")  # Removes banana
print(thisset)
```

**Example 28b: update() Method**
```python
thisset = {"apple", "banana", "cherry"}
tropical = {"pineapple", "mango", "papaya"}

# Add all elements from tropical to thisset
thisset.update(tropical)
print(thisset)  # {'apple', 'banana', 'cherry', 'pineapple', 'mango', 'papaya'}

# update() can also take lists, tuples, etc.
thisset.update([1, 2, 3])
print(thisset)
```

**Example 28c: True and 1 are Considered the Same**
```python
thisset = {"apple", "banana", "cherry", True, 1, 2}
print(thisset)  # {True, 2, 'cherry', 'apple', 'banana'}
# Notice: only one True/1 appears!

thisset2 = {False, 0, "hello"}
print(thisset2)  # {False, 'hello'}
# Notice: False and 0 are also treated as duplicates
```

**Example 28d: symmetric_difference() - XOR Operation**
```python
x = {"apple", "banana", "cherry"}
y = {"google", "microsoft", "apple"}

# Elements in either set, but NOT in both
z = x.symmetric_difference(y)
print(z)  # {'google', 'microsoft', 'banana', 'cherry'}

# Using ^ operator
z = x ^ y
print(z)  # Same result
```

**Common Set Operations:**
- `union()` or `|`: Combine sets
- `intersection()` or `&`: Common elements
- `difference()` or `-`: Elements in first but not in second
- `symmetric_difference()` or `^`: Elements in either but not both
- `update()`: Add elements from another set
- `discard()`: Remove element (no error if not found)
- `remove()`: Remove element (raises error if not found)

---

## 10. Dictionaries

Dictionaries store key-value pairs. They are mutable and unordered (in Python 3.7+, they maintain insertion order).

### Creating Dictionaries

**Example 30: Three Ways to Create Dictionaries**
```python
# Method 1: Literal notation
# a = {
#     'id': "21BD021315",
#     'name': 'Student 1',
#     'age': 18,
#     'gpa': 4.0
# }

# Method 2: Using dict() constructor
# a = dict(id='21BD021315', name='Student 1', age=18, gpa=4.0)

# Method 3: Empty dict and adding keys
a = dict()
a['id'] = '21BD021315'
a['name'] = 'Student 1'

print(a['name'])  # Student 1
```

### Dictionary Methods

**Example 31: Working with Dictionaries**
```python
a = ['hello', 'world', 'abc', 'hello', 'world', 'hello']

# Counting occurrences using dictionary
d = dict()

for s in a:
    if s not in d:
        d[s] = 0
    d[s] += 1

# Iterating over keys
for key in d:
    print(key, d[key])

# Dictionary methods
# d.pop('hello')  # Remove key
# print(d.keys())    # Get all keys
# print(d.values())  # Get all values
# print(d.items())   # Get all key-value pairs

# Iterating over items
for key, value in d.items():
    print(f'{key} ---> {value}')
```

**Example 31a: Accessing Dictionary Values with get()**
```python
thisdict = {"brand": "Ford", "model": "Mustang", "year": 1964}

# Access with bracket notation
x = thisdict["model"]
print(x)  # Mustang

# Access with get() - safer!
x = thisdict.get("model")
print(x)  # Mustang

# Benefit: get() doesn't raise error if key doesn't exist
# thisdict["price"]  # This would raise KeyError!
x = thisdict.get("price", "Not found")
print(x)  # Not found
```

**Example 31b: Changing and Adding Dictionary Items**
```python
thisdict = {"brand": "Ford", "model": "Mustang", "year": 1964}

# Changing values
thisdict["year"] = 2018
print(thisdict)

# Adding new items
thisdict["color"] = "red"
print(thisdict)  # {'brand': 'Ford', 'model': 'Mustang', 'year': 2018, 'color': 'red'}
```

**Example 31c: update() Method**
```python
thisdict = {"brand": "Ford", "model": "Mustang", "year": 1964}

# Update existing and add new keys
thisdict.update({"year": 2020, "color": "red"})
print(thisdict)

# Update can also merge two dictionaries
dict1 = {"a": 1, "b": 2}
dict2 = {"c": 3, "d": 4}
dict1.update(dict2)
print(dict1)  # {'a': 1, 'b': 2, 'c': 3, 'd': 4}
```

**Example 31d: Nested Dictionaries**
```python
# Dictionary of dictionaries
myfamily = {
    "child1": {"name": "Emil", "year": 2004},
    "child2": {"name": "Tobias", "year": 2007},
    "child3": {"name": "Linus", "year": 2011}
}

# Accessing nested values
print(myfamily["child2"]["name"])  # Tobias
print(myfamily["child1"]["year"])  # 2004

# Iterating over nested dictionaries
for child, info in myfamily.items():
    print(f"{child}:")
    for key, value in info.items():
        print(f"  {key}: {value}")
```

**Example 31e: Dictionary Comprehension**
```python
# Create dictionary from list
items = ['apple', 'banana', 'cherry']
prices = {item: len(item) for item in items}
print(prices)  # {'apple': 5, 'banana': 6, 'cherry': 6}

# Dictionary comprehension with condition
squares = {x: x**2 for x in range(6) if x % 2 == 0}
print(squares)  # {0: 0, 2: 4, 4: 16}

# Create dict from two lists
keys = ['a', 'b', 'c']
values = [1, 2, 3]
combined = {keys[i]: values[i] for i in range(len(keys))}
print(combined)  # {'a': 1, 'b': 2, 'c': 3}
```

**Common Dictionary Methods:**
- `keys()`: Returns all keys
- `values()`: Returns all values
- `items()`: Returns key-value pairs
- `get(key, default)`: Safely get value
- `pop(key)`: Remove and return value
- `update(other_dict)`: Merge dictionaries
- `clear()`: Remove all items
- `copy()`: Create a shallow copy

---

## 11. 2D Arrays (Nested Lists)

**Example 33: Reading and Working with 2D Arrays**
```python
# Input format:
# 4
# 1 2 3 4
# 1 2 3 4
# 1 2 3 4
# 1 2 3 4

n = int(input())

arr = []

# Reading 2D array
for i in range(n):
    nums = [int(n) for n in input().split(' ')]
    arr.append(nums)

# Printing 2D array
for row in arr:
    print(row)
```

---

## 12. Additional Topics

### Random Module

**Example 32: Generating Random Numbers**
```python
import random

print(random.randint(0, 100))  # Random integer between 0 and 100
```

---

## Summary

### Key Takeaways

**Collections Comparison:**

| Type | Ordered | Mutable | Allows Duplicates | Syntax |
|------|---------|---------|-------------------|--------|
| List | Yes | Yes | Yes | `[1, 2, 3]` |
| Tuple | Yes | No | Yes | `(1, 2, 3)` |
| Set | No | Yes | No | `{1, 2, 3}` |
| Dictionary | Yes (3.7+) | Yes | Keys: No, Values: Yes | `{'a': 1}` |

**Loop Comparison:**

```python
# While loop: when you don't know iterations in advance
while condition:
    # code

# For loop: when iterating over sequences
for item in sequence:
    # code

# For loop with range: when you know number of iterations
for i in range(n):
    # code
```

**When to Use Each Collection:**
- **List**: Ordered sequence, need indexing, allow duplicates
- **Tuple**: Immutable sequence, use as dict keys
- **Set**: Unique elements, fast membership testing
- **Dictionary**: Key-value pairs, fast lookups

---

