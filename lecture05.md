# Lecture 5: Advanced Python Constructs

## Plan
- Iterators
- Generators (yield)
- Variable scope (local/global/nonlocal)
- Modules & packages (import)
- Working with dates (datetime)
- Math operations (math, random)
- JSON: parsing & serialization

---

## 1. Iterators

An **iterator** is an object that implements the iterator protocol — two special methods: `__iter__()` and `__next__()`. Iterators allow you to traverse through all elements of a collection one at a time without loading everything into memory.

### How Iteration Works Under the Hood

When you write a `for` loop, Python:
1. Calls `iter()` on the object to get an iterator
2. Repeatedly calls `next()` on the iterator to get each value
3. Stops when `StopIteration` exception is raised

```python
nums = [10, 20, 30]

# This for loop:
for n in nums:
    print(n)

# Is equivalent to:
it = iter(nums)
print(next(it))  # 10
print(next(it))  # 20
print(next(it))  # 30
# next(it) would raise StopIteration
```

### Built-in Iterables vs Iterators

An **iterable** is any object that can return an iterator (has `__iter__`). An **iterator** is an object that produces values one by one (has both `__iter__` and `__next__`).

```python
my_list = [1, 2, 3]       # iterable, NOT an iterator
my_iter = iter(my_list)    # iterator

print(type(my_list))   # <class 'list'>
print(type(my_iter))   # <class 'list_iterator'>

print(next(my_iter))   # 1
print(next(my_iter))   # 2
print(next(my_iter))   # 3
```

### Creating a Custom Iterator

You can make any class iterable by implementing `__iter__()` and `__next__()`.

**Example 1: Countdown Iterator**

```python
class Countdown:
    def __init__(self, start):
        self.current = start

    def __iter__(self):
        return self

    def __next__(self):
        if self.current <= 0:
            raise StopIteration
        value = self.current
        self.current -= 1
        return value

for num in Countdown(5):
    print(num)
# Output: 5 4 3 2 1
```

**Example 2: Even Numbers Iterator**

```python
class EvenNumbers:
    def __init__(self, limit):
        self.limit = limit
        self.current = 0

    def __iter__(self):
        return self

    def __next__(self):
        self.current += 2
        if self.current > self.limit:
            raise StopIteration
        return self.current

evens = EvenNumbers(10)
print(list(evens))  # [2, 4, 6, 8, 10]
```

**Example 3: Infinite Iterator with `islice`**

Iterators can be infinite — they never raise `StopIteration`. Use `itertools.islice` to take a finite number of elements.

```python
from itertools import islice

class InfiniteCounter:
    def __init__(self, start=0, step=1):
        self.current = start
        self.step = step

    def __iter__(self):
        return self

    def __next__(self):
        value = self.current
        self.current += self.step
        return value

counter = InfiniteCounter(start=1, step=3)
first_five = list(islice(counter, 5))
print(first_five)  # [1, 4, 7, 10, 13]
```

**Example 4: Prime Numbers Iterator (Infinite)**

An iterator that generates prime numbers indefinitely. Combined with `islice`, you can take as many as you need:

```python
import math
from itertools import islice

class PrimeNumbers:
    def __init__(self):
        self.current = 2

    def next_prime(self):
        found = False
        while not found:
            found = True
            self.current += 1
            for i in range(2, int(math.sqrt(self.current)) + 1):
                if self.current % i == 0:
                    found = False
                    break
        return self.current

    def __iter__(self):
        return self

    def __next__(self):
        value = self.current
        self.current = self.next_prime()
        return value

a = PrimeNumbers()
b = iter(a)
print(next(b))  # 2
print(next(b))  # 3
print(next(b))  # 5

# islice consumes the iterator — it continues from where it left off
print(list(islice(b, 3)))  # [7, 11, 13]
print(list(islice(b, 3)))  # [17, 19, 23]
```

### The `iter()` Function with a Sentinel

`iter()` can accept two arguments: a callable and a sentinel value. It calls the callable repeatedly until the sentinel is returned.

```python
import random

random.seed(42)

# Roll a die until we get a 6
rolls = iter(lambda: random.randint(1, 6), 6)
print(list(rolls))  # all rolls before the first 6
```

---

## 2. Generators (yield)

A **generator** is a special type of iterator defined using a function with the `yield` keyword. Generators produce values **lazily** — one at a time, only when requested — making them memory-efficient for large or infinite sequences.

### Basic Generator Function

When a function contains `yield`, calling it does not execute the body. Instead it returns a generator object. The body runs only when you call `next()` or iterate over it.

```python
def my_generator():
    print("First")
    yield 1
    print("Second")
    yield 2
    print("Third")
    yield 3

gen = my_generator()
print(type(gen))    # <class 'generator'>

print(next(gen))    # prints "First", returns 1
print(next(gen))    # prints "Second", returns 2
print(next(gen))    # prints "Third", returns 3
# next(gen) would raise StopIteration
```

### Generator vs Regular Function

```python
# Regular function — builds the entire list in memory
def get_squares_list(n):
    result = []
    for i in range(n):
        result.append(i ** 2)
    return result

# Generator — produces values one at a time
def get_squares_gen(n):
    for i in range(n):
        yield i ** 2

# Both produce the same values
print(list(get_squares_list(5)))  # [0, 1, 4, 9, 16]
print(list(get_squares_gen(5)))   # [0, 1, 4, 9, 16]
```

The generator version uses far less memory, especially for large `n`.

### Generator Expressions

Just like list comprehensions, but with parentheses instead of brackets. They create generators without a function definition.

```python
# List comprehension — creates entire list in memory
squares_list = [x ** 2 for x in range(10)]

# Generator expression — lazy, produces values on demand
squares_gen = (x ** 2 for x in range(10))

print(type(squares_list))  # <class 'list'>
print(type(squares_gen))   # <class 'generator'>

print(sum(squares_gen))    # 285 (consumed lazily)
```

### Practical Examples

**Example 4: Fibonacci Generator**

```python
def fibonacci():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

from itertools import islice

fib = fibonacci()
first_10 = list(islice(fib, 10))
print(first_10)  # [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
```

**Example 5: Reading a Large File Line by Line**

```python
def read_lines(filename):
    with open(filename, 'r') as f:
        for line in f:
            yield line.strip()

# Usage: processes one line at a time, never loads entire file
# for line in read_lines("huge_file.txt"):
#     process(line)
```

**Example 6: Pipeline of Generators**

Generators can be chained together to form processing pipelines:

```python
def numbers(n):
    for i in range(1, n + 1):
        yield i

def doubled(gen):
    for value in gen:
        yield value * 2

def only_greater_than(gen, threshold):
    for value in gen:
        if value > threshold:
            yield value

# Pipeline: numbers -> double -> filter > 10
pipeline = only_greater_than(doubled(numbers(10)), 10)
print(list(pipeline))  # [12, 14, 16, 18, 20]
```

### `yield from` — Delegating to a Sub-generator

The `yield from` expression delegates iteration to another iterable or generator:

```python
def inner():
    yield 1
    yield 2
    yield 3

def outer():
    yield "start"
    yield from inner()  # delegates to inner()
    yield "end"

print(list(outer()))  # ['start', 1, 2, 3, 'end']
```

**Example 7: Flatten Nested Lists with `yield from`**

```python
def flatten(nested):
    for item in nested:
        if isinstance(item, list):
            yield from flatten(item)
        else:
            yield item

data = [1, [2, 3], [4, [5, 6]], 7]
print(list(flatten(data)))  # [1, 2, 3, 4, 5, 6, 7]
```

---

## 3. Variable Scope (local / global / nonlocal)

**Scope** determines where a variable can be accessed. Python follows the **LEGB rule** for name resolution:

| Scope | Description |
|-------|-------------|
| **L** — Local | Variables defined inside the current function |
| **E** — Enclosing | Variables in the enclosing (outer) function (for nested functions) |
| **G** — Global | Variables defined at the module (file) level |
| **B** — Built-in | Names pre-defined in Python (`print`, `len`, `range`, etc.) |

Python searches for a name in this order: Local → Enclosing → Global → Built-in.

### Local Scope

Variables defined inside a function exist only within that function:

```python
def greet():
    message = "Hello!"  # local variable
    print(message)

greet()          # Hello!
# print(message)  # NameError: name 'message' is not defined
```

### Global Scope

Variables defined at the module level are accessible everywhere in the file:

```python
language = "Python"  # global variable

def show():
    print(language)  # reading global — OK

show()  # Python
```

### The `global` Keyword

To **modify** a global variable inside a function, you must declare it with `global`:

```python
counter = 0

def increment():
    global counter
    counter += 1

increment()
increment()
increment()
print(counter)  # 3
```

Without `global`, assigning to `counter` would create a new local variable and leave the global unchanged (or raise `UnboundLocalError` if you try to read it before assigning).

**Example 8: UnboundLocalError Trap**

```python
x = 10

def broken():
    print(x)  # UnboundLocalError! Python sees the assignment below
    x = 20    # and treats x as local for the entire function

# broken()  # UnboundLocalError: cannot access local variable 'x'
```

### The `nonlocal` Keyword

`nonlocal` is used in **nested functions** to modify a variable from the enclosing (outer) function's scope:

```python
def outer():
    count = 0

    def inner():
        nonlocal count
        count += 1
        print(f"count = {count}")

    inner()  # count = 1
    inner()  # count = 2
    inner()  # count = 3
    print(f"final count = {count}")  # final count = 3

outer()
```

### `nonlocal` vs `global`

```python
x = "global"

def outer():
    x = "outer"

    def inner_global():
        global x
        x = "modified by inner_global"

    def inner_nonlocal():
        nonlocal x
        x = "modified by inner_nonlocal"

    inner_nonlocal()
    print(f"outer x: {x}")  # outer x: modified by inner_nonlocal

outer()
print(f"global x: {x}")  # global x: global

# Now call inner_global through outer
def outer2():
    x = "outer2"

    def inner_global():
        global x
        x = "modified by inner_global"

    inner_global()
    print(f"outer2 x: {x}")  # outer2 x: outer2 (unchanged!)

outer2()
print(f"global x: {x}")  # global x: modified by inner_global
```

**Example 9: Closure with `nonlocal` — Counter Factory**

```python
def make_counter(start=0):
    count = start

    def increment():
        nonlocal count
        count += 1
        return count

    def decrement():
        nonlocal count
        count -= 1
        return count

    def get():
        return count

    return increment, decrement, get

inc, dec, get = make_counter(10)
print(inc())  # 11
print(inc())  # 12
print(dec())  # 11
print(get())  # 11
```

---

## 4. Modules & Packages (import)

A **module** is simply a Python file (`.py`) that contains definitions (functions, classes, variables). A **package** is a directory containing modules and an `__init__.py` file.

### Why Use Modules?
- **Organization**: Split code into logical, manageable files
- **Reusability**: Write once, import anywhere
- **Namespace isolation**: Avoid name collisions between different parts of your code

### Importing a Module

```python
import math

print(math.pi)         # 3.141592653589793
print(math.sqrt(16))   # 4.0
```

### Importing Specific Names

```python
from math import pi, sqrt

print(pi)         # 3.141592653589793
print(sqrt(16))   # 4.0
```

### Importing with an Alias

```python
import math as m

print(m.pi)       # 3.141592653589793
print(m.sqrt(25)) # 5.0
```

```python
from datetime import datetime as dt

now = dt.now()
print(now)
```

### Importing Everything (Not Recommended)

```python
from math import *  # imports all public names

print(pi)
print(sqrt(9))
```

**Warning**: `from module import *` pollutes the namespace and makes it hard to know where names come from. Avoid in production code.

### Creating Your Own Module

**Example 10: Custom Module**

Create a file `mymath.py`:

```python
# mymath.py

def add(a, b):
    return a + b

def multiply(a, b):
    return a * b

PI = 3.14159
```

Use it in another file:

```python
# main.py
import mymath

print(mymath.add(3, 5))       # 8
print(mymath.multiply(4, 6))  # 24
print(mymath.PI)               # 3.14159
```

Or import specific names:

```python
from mymath import add, PI

print(add(10, 20))  # 30
print(PI)            # 3.14159
```

### Packages (Directories of Modules)

A **package** is a directory containing:
- An `__init__.py` file (can be empty)
- One or more module files

```
my_package/
    __init__.py
    utils.py
    models.py
```

```python
# Using the package
from my_package import utils
from my_package.models import User
```

### The `__name__` Variable

Every module has a special variable `__name__`:
- If the module is run directly: `__name__ == "__main__"`
- If the module is imported: `__name__ == "module_name"`

```python
# greetings.py

def hello():
    print("Hello from greetings!")

if __name__ == "__main__":
    # This code only runs when the file is executed directly
    # It does NOT run when the file is imported
    print("Running greetings.py directly")
    hello()
```

```python
# main.py
import greetings

greetings.hello()  # "Hello from greetings!"
# The "Running greetings.py directly" message does NOT appear
```

### Useful Built-in Modules

| Module | Purpose |
|--------|---------|
| `math` | Mathematical functions |
| `random` | Random number generation |
| `datetime` | Date and time operations |
| `json` | JSON encoding/decoding |
| `os` | Operating system interface |
| `sys` | System-specific parameters |
| `collections` | Specialized container datatypes |
| `itertools` | Iterator building blocks |

---

## 5. Working with Dates (datetime)

The `datetime` module provides classes for working with dates and times.

### Key Classes

| Class | Description |
|-------|-------------|
| `datetime.date` | A date (year, month, day) |
| `datetime.time` | A time (hour, minute, second, microsecond) |
| `datetime.datetime` | A combination of date and time |
| `datetime.timedelta` | A duration — the difference between two dates/times |

### Getting the Current Date and Time

```python
from datetime import datetime, date, time, timedelta

now = datetime.now()
print(now)             # 2026-02-19 14:30:45.123456
print(now.year)        # 2026
print(now.month)       # 2
print(now.day)         # 19
print(now.hour)        # 14
print(now.minute)      # 30
print(now.second)      # 45

today = date.today()
print(today)           # 2026-02-19
```

### Creating Date and Time Objects

```python
from datetime import datetime, date, time

# Create a specific date
birthday = date(2000, 5, 15)
print(birthday)  # 2000-05-15

# Create a specific time
alarm = time(7, 30, 0)
print(alarm)  # 07:30:00

# Create a specific datetime
event = datetime(2026, 12, 31, 23, 59, 59)
print(event)  # 2026-12-31 23:59:59
```

### Formatting Dates with `strftime()`

The `strftime()` method converts a datetime to a formatted string.

| Code | Meaning | Example |
|------|---------|---------|
| `%Y` | Year (4 digits) | 2026 |
| `%m` | Month (01-12) | 02 |
| `%d` | Day (01-31) | 19 |
| `%H` | Hour 24h (00-23) | 14 |
| `%M` | Minute (00-59) | 30 |
| `%S` | Second (00-59) | 45 |
| `%A` | Weekday name | Thursday |
| `%B` | Month name | February |
| `%I` | Hour 12h (01-12) | 02 |
| `%p` | AM/PM | PM |

```python
from datetime import datetime

now = datetime.now()

print(now.strftime("%Y-%m-%d"))           # 2026-02-19
print(now.strftime("%d/%m/%Y"))           # 19/02/2026
print(now.strftime("%A, %B %d, %Y"))      # Thursday, February 19, 2026
print(now.strftime("%I:%M %p"))           # 02:30 PM
print(now.strftime("%H:%M:%S"))           # 14:30:45
```

### Parsing Strings with `strptime()`

The `strptime()` method converts a string to a datetime object.

```python
from datetime import datetime

date_str = "2026-02-19 14:30:00"
dt = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
print(dt)        # 2026-02-19 14:30:00
print(dt.year)   # 2026

date_str2 = "19/02/2026"
dt2 = datetime.strptime(date_str2, "%d/%m/%Y")
print(dt2)       # 2026-02-19 00:00:00
```

### Date Arithmetic with `timedelta`

`timedelta` represents a duration and supports addition/subtraction with dates.

```python
from datetime import datetime, timedelta

now = datetime.now()

# Add time
tomorrow = now + timedelta(days=1)
next_week = now + timedelta(weeks=1)
two_hours_later = now + timedelta(hours=2, minutes=30)

print(f"Now:             {now}")
print(f"Tomorrow:        {tomorrow}")
print(f"Next week:       {next_week}")
print(f"2.5 hours later: {two_hours_later}")

# Subtract time
yesterday = now - timedelta(days=1)
print(f"Yesterday:       {yesterday}")
```

**Example 11: Days Until a Date**

```python
from datetime import date

today = date.today()
new_year = date(today.year + 1, 1, 1)

diff = new_year - today
print(f"Days until New Year: {diff.days}")
```

**Example 12: Age Calculator**

```python
from datetime import date

def calculate_age(birth_date):
    today = date.today()
    age = today.year - birth_date.year
    # Check if birthday hasn't occurred yet this year
    if (today.month, today.day) < (birth_date.month, birth_date.day):
        age -= 1
    return age

birthday = date(2000, 5, 15)
print(f"Age: {calculate_age(birthday)}")  # Age: 25
```

### Comparing Dates

```python
from datetime import date

date1 = date(2026, 1, 1)
date2 = date(2026, 12, 31)

print(date1 < date2)   # True
print(date1 == date2)  # False
print(date1 > date2)   # False

dates = [date(2026, 3, 15), date(2026, 1, 1), date(2026, 7, 4)]
print(sorted(dates))   # [2026-01-01, 2026-03-15, 2026-07-04]
print(min(dates))      # 2026-01-01
print(max(dates))      # 2026-07-04
```

---

## 6. Math Operations (math, random)

### The `math` Module

The `math` module provides mathematical functions and constants.

### Constants

```python
import math

print(math.pi)    # 3.141592653589793
print(math.e)     # 2.718281828459045
```

### Common Functions

```python
import math

print(min(1, 2, 3, 4))

# Rounding
print(math.floor(4.7))    # 4 (round down)
print(math.ceil(4.2))     # 5 (round up)
print(math.trunc(4.9))    # 4 (remove decimal part)
print(round(2.5))
# Power and logarithms
print(math.pow(2, 10))    # 1024.0
print(math.sqrt(144))     # 12.0
print(math.log(math.e))   # 1.0 (natural log)
print(math.log2(1024))    # 10.0
print(math.log10(1000))   # 3.0

# Absolute value
print(math.fabs(-42))     # 42.0

# Factorial and GCD
print(math.factorial(5))  # 120 (5! = 5*4*3*2*1)
print(math.gcd(24, 36))   # 12

# Trigonometry (arguments in radians)
print(math.sin(math.pi / 2))   # 1.0
print(math.cos(0))              # 1.0
print(math.tan(math.pi / 4))   # ~1.0

# Convert between degrees and radians
print(math.degrees(math.pi))    # 180.0
print(math.radians(180))        # 3.141592653589793
```

**Example 13: Distance Between Two Points**

```python
import math

def distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

# or use math.dist (Python 3.8+)
def distance_v2(p1, p2):
    return math.dist(p1, p2)

print(distance(0, 0, 3, 4))            # 5.0
print(distance_v2((0, 0), (3, 4)))     # 5.0
```

**Example 14: Check if a Number is a Perfect Square**

```python
import math

def is_perfect_square(n):
    if n < 0:
        return False
    root = math.isqrt(n)
    return root * root == n

print(is_perfect_square(16))   # True
print(is_perfect_square(15))   # False
print(is_perfect_square(144))  # True
```

### The `random` Module

The `random` module generates pseudo-random numbers.

### Basic Random Functions

```python
import random

# Random float between 0.0 and 1.0
print(random.random())          # e.g., 0.7134

# Random float in a range
print(random.uniform(1.5, 9.5)) # e.g., 6.234

# Random integer in a range (inclusive)
print(random.randint(1, 100))   # e.g., 42

# Random integer in a range (exclusive end), with optional step
print(random.randrange(0, 100, 5))  # e.g., 35 (multiples of 5)
```

### Working with Sequences

```python
import random

fruits = ["apple", "banana", "cherry", "date", "elderberry"]

# Pick a random element
print(random.choice(fruits))     # e.g., "cherry"

# Pick multiple random elements (with replacement)
print(random.choices(fruits, k=3))  # e.g., ["apple", "date", "apple"]

# Pick multiple random elements (without replacement)
print(random.sample(fruits, k=3))   # e.g., ["banana", "date", "cherry"]

# Shuffle a list in place
random.shuffle(fruits)
print(fruits)  # e.g., ["date", "cherry", "apple", "elderberry", "banana"]
```

**Example 15: Random Password Generator**

```python
import random
import string

def generate_password(length=12):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choices(characters, k=length))
    return password

print(generate_password())     # e.g., "kA3$mP9!xL2@"
print(generate_password(20))   # e.g., "Hj7&kL2!mN4@pQ8#rT0%"
```

**Example 16: Dice Roller Simulation**

```python
import random

def roll_dice(num_dice=2, sides=6):
    rolls = [random.randint(1, sides) for _ in range(num_dice)]
    return rolls, sum(rolls)

rolls, total = roll_dice()
print(f"Rolls: {rolls}, Total: {total}")
# e.g., Rolls: [3, 5], Total: 8

### Setting a Seed for Reproducibility

```python
import random

random.seed(42)
print(random.randint(1, 100))  # always 82
print(random.randint(1, 100))  # always 15

random.seed(42)
print(random.randint(1, 100))  # 82 again (same seed = same sequence)
print(random.randint(1, 100))  # 15 again
```

---

## 7. JSON: Parsing & Serialization

**JSON** (JavaScript Object Notation) is a lightweight text format for data exchange. It's the most common format for APIs and configuration files.

### JSON Data Types

| JSON Type | Python Type |
|-----------|-------------|
| `object` `{}` | `dict` |
| `array` `[]` | `list` |
| `string` `""` | `str` |
| `number` (int) | `int` |
| `number` (float) | `float` |
| `true` / `false` | `True` / `False` |
| `null` | `None` |

### The `json` Module

Python's built-in `json` module handles JSON encoding and decoding.

### Converting Python to JSON (`json.dumps`)

`json.dumps()` converts a Python object to a JSON string.

```python
import json

data = {
    "name": "Askar",
    "age": 25,
    "courses": ["PP2", "Algorithms", "Databases"],
    "graduated": False,
    "gpa": 3.8
}

json_string = json.dumps(data)
print(json_string)
# {"name": "Askar", "age": 25, "courses": ["PP2", "Algorithms", "Databases"], "graduated": false, "gpa": 3.8}
print(type(json_string))  # <class 'str'>
```

### Pretty-Printing JSON

```python
import json

data = {
    "name": "Askar",
    "age": 25,
    "courses": ["PP2", "Algorithms", "Databases"]
}

pretty = json.dumps(data, indent=4)
print(pretty)
# {
#     "name": "Askar",
#     "age": 25,
#     "courses": [
#         "PP2",
#         "Algorithms",
#         "Databases"
#     ]
# }
```

### Sorting Keys

```python
import json

data = {"banana": 3, "apple": 5, "cherry": 1}
print(json.dumps(data, sort_keys=True, indent=2))
# {
#   "apple": 5,
#   "banana": 3,
#   "cherry": 1
# }
```

### Converting JSON to Python (`json.loads`)

`json.loads()` parses a JSON string into a Python object.

```python
import json

json_string = '{"name": "Askar", "age": 25, "courses": ["PP2", "Algorithms"]}'

data = json.loads(json_string)
print(data)               # {'name': 'Askar', 'age': 25, 'courses': ['PP2', 'Algorithms']}
print(type(data))         # <class 'dict'>
print(data["name"])       # Askar
print(data["courses"][0]) # PP2
```

### Reading JSON from a File (`json.load`)

```python
import json

# Reading JSON file
with open("data.json", "r") as f:
    data = json.load(f)

print(data)
```

### Writing JSON to a File (`json.dump`)

```python
import json

data = {
    "students": [
        {"name": "Alice", "gpa": 3.9},
        {"name": "Bob", "gpa": 3.5},
        {"name": "Charlie", "gpa": 4.0}
    ]
}

with open("students.json", "w") as f:
    json.dump(data, f, indent=4)
```

### Note: `dumps`/`loads` vs `dump`/`load`

| Function | Input/Output | Purpose |
|----------|-------------|---------|
| `json.dumps()` | → string | Python object → JSON **s**tring |
| `json.loads()` | ← string | JSON **s**tring → Python object |
| `json.dump()` | → file | Python object → JSON **f**ile |
| `json.load()` | ← file | JSON **f**ile → Python object |

The **s** in `dumps`/`loads` stands for **string**.

**Example 17: Working with Nested JSON**

```python
import json

json_string = '''
{
    "university": "KBTU",
    "departments": [
        {
            "name": "FIT",
            "students": 500,
            "courses": ["PP2", "Algorithms", "OS"]
        },
        {
            "name": "FOGI",
            "students": 300,
            "courses": ["Geology", "Mining", "GIS"]
        }
    ]
}
'''

data = json.loads(json_string)

# Access nested data
for dept in data["departments"]:
    print(f"{dept['name']}: {dept['students']} students")
    print(f"  Courses: {', '.join(dept['courses'])}")
# FIT: 500 students
#   Courses: PP2, Algorithms, OS
# FOGI: 300 students
#   Courses: Geology, Mining, GIS
```

**Example 18: Converting Custom Objects to JSON**

## Conclusion

### Key Takeaways

**Iterators**:
- An iterator implements `__iter__()` and `__next__()`
- `iter()` gets an iterator from an iterable, `next()` gets the next value
- `StopIteration` signals the end of iteration
- Custom iterators allow you to define your own iteration logic

**Generators**:
- Generators are functions that use `yield` instead of `return`
- They produce values lazily — one at a time, on demand
- Generator expressions use `()` instead of `[]`
- `yield from` delegates to another generator or iterable
- Generators are memory-efficient for large or infinite sequences

**Variable Scope**:
- Python uses the LEGB rule: Local → Enclosing → Global → Built-in
- Use `global` to modify a module-level variable inside a function
- Use `nonlocal` to modify an enclosing function's variable in a nested function
- Avoid overusing `global` — prefer passing arguments and returning values

**Modules & Packages**:
- A module is a `.py` file; a package is a directory with `__init__.py`
- Use `import`, `from ... import`, or `import ... as` to bring in modules
- `__name__ == "__main__"` distinguishes direct execution from imports
- Python has many useful built-in modules (`math`, `random`, `datetime`, `json`, etc.)

**datetime**:
- Use `datetime.now()` and `date.today()` for current date/time
- `strftime()` formats dates to strings, `strptime()` parses strings to dates
- `timedelta` represents durations and supports date arithmetic

**math & random**:
- `math` provides constants (`pi`, `e`) and functions (`sqrt`, `log`, `sin`, `factorial`, etc.)
- `random` generates pseudo-random numbers and works with sequences
- Use `random.seed()` for reproducible results

**JSON**:
- `json.dumps()` / `json.dump()` — Python → JSON (string / file)
- `json.loads()` / `json.load()` — JSON → Python (string / file)
- Use `indent` for pretty-printing, `sort_keys` for sorted output
