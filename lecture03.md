# Lecture 3: Functions, Lambda, and OOP

## Plan
- Functions
- Lambda functions
- Classes and objects
- Inheritance

---

## Functions

### Basic Function

```python
def func():
    print("Hello!")

func()
```

### Functions with Arguments

```python
def func(arg1, arg2):
    print(arg1 + arg2)

func(3, 5)
func(arg1 = "hello ", arg2 = "all")
func([1, 2, 3], [4, 5, 6])
```

### Modifying Mutable Arguments

```python
def func(my_list):
    my_list[0] = 'hello'
    my_list[2] = 'world'

    for item in my_list:
        print(item)

l = [1, 2, 10, 20, 30]
func(l)
print(l)  # List is modified!
```

### *args (Variable Positional Arguments)

```python
def func(a, *args):
    for arg in args:
        print(arg, type(arg))

func([1, 2, 3], "hello", 10)
func(1, 2, 3, 4, 5)
```

### Using *args for Sum

```python
def my_sum(*args):
    result = 0
    for x in args:
        result += x
    return result

sum1 = my_sum(1, 2, 3, 4, 5)
sum2 = my_sum(1, 2, 3)
print(sum1)  # 15
print(sum2)  # 6
```

### Return Values

```python
def func1(num1, num2):
    print(num1 + num2)

def func2(num1, num2):
    return num1 + num2

print(func1(3, 5))  # None - func1 does not return anything
print(func2(3, 5))  # 8
```

### Default Parameter Values

```python
def func(num1 = 0, num2 = 0):
    print(num1 + num2)

func()       # 0
func(3)      # 3
func(3, 5)   # 8
```

### **kwargs (Variable Keyword Arguments)

```python
def func(**kwargs):
    print(kwargs)  # kwargs is a dict
    for key in kwargs:
        print(key, kwargs[key])

func(fname = "Askar", lname = "Akshabayev")
```

### Global Variables

```python
x = 1  # global variable

def func():
    print(x)

func()
```

### Local Variables

```python
x = 1  # global variable

def func():
    x = 2  # local variable
    print(x)

func()  # prints 2
```

### Using `global` Keyword

```python
x = 1  # global variable

def func():
    global x  # allows to modify x within a function
    x += 1
    print(x)

func()
print(x)  # x is now 2
```

### Finding Maximum Value

```python
def f(a, b, c):
    if a >= b and a >= c:
        return a
    elif b >= a and b >= c:
        return b
    return c

maxi = f(3, 8, 5)
print(maxi)  # 8
```

### Returning Multiple Values

```python
def f(a, b):
    result1 = a * b
    result2 = a + b
    result3 = a - b
    return result1, result2, result3

a, b, c = f(2, 3)
a, _, _ = f(2, 3)  # only need first value
_, a, _ = f(2, 3)  # only need second value
a, _, c = f(2, 3)  # need first and third
print(a, c)
```

### Recursion with Memoization

```python
result = dict()

def rec(n):
    if n in result:
        return result[n]

    if n == 0 or n == 1:
        return 1
    result[n] = rec(n - 1) + rec(n - 2)
    return result[n]

print(rec(5))
```

---

## Lambda Functions

Lambda functions are a quicker way to write functions on the fly using the `lambda` keyword.

### Basic Lambda

```python
my_power = lambda x, y: x ** y
print(my_power(2, 3))  # 8
```

### map() with Lambda

The `map` function takes a function and a sequence, applying the function over all elements.

```python
nums = [48, 6, 9, 21, 1]
square_all = map(lambda num: num ** 2, nums)
print(list(square_all))  # [2304, 36, 81, 441, 1]
```

### Function Returning Lambda

```python
def func(n):
    return lambda a: a * n

doubler = func(2)      # lambda a: a * 2
print(doubler(3))      # 6
print(doubler(6))      # 12

triple = func(3)       # lambda a: a * 3
print(triple(3))       # 9
print(triple(6))       # 18

multiple_100 = func(100)  # lambda a: a * 100
print(multiple_100(5))    # 500
print(multiple_100(6))    # 600
```

### filter() with Lambda

Filter even numbers from a list:

```python
list1 = [2, 3, 5, 8, 16, 100, 103]
list2 = list(filter(lambda x: x % 2 == 0, list1))
print(list2)  # [2, 8, 16, 100]
```

Filter prime numbers from a list:

```python
def is_prime(n):
    if n == 1:
        return False
    for i in range(2, n):
        if n % i == 0:
            return False
    return True

list1 = [1, 2, 14, 5, 13, 100, 103]
list2 = list(filter(lambda x: is_prime(x), list1))
print(list2)  # [2, 5, 13, 103]
```

---

## OOP (Object-Oriented Programming)

### Basic Class

```python
class MyClass:
    # fields
    x = 5
    y = 6

    # methods
    def sum(self, a, b):
        return self.x + self.y + a + b

a = MyClass()
a.x = 10
a.y = 20

b = MyClass()
b.x = 7
b.y = 30

print(a.x, a.y)      # 10 20
print(b.x, b.y)      # 7 30
print(a.sum(1, 2))   # 33 (10 + 20 + 1 + 2)
print(b.sum(3, 4))   # 44 (7 + 30 + 3 + 4)
```

### Inheritance

```python
class Person:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname

    def show(self):
        print(f'{self.name} - {self.surname}')


class Student(Person):
    def __init__(self, name, surname, gpa, faculty):
        super().__init__(name, surname)  # Call parent constructor
        self.gpa = gpa
        self.faculty = faculty

    def show(self):
        super().show()  # Call parent method
        print(f'{self.gpa} - {self.faculty}')


a = Student("Aaa", "Bbb", 3.9, "FIT")
a.show()
# Output:
# Aaa - Bbb
# 3.9 - FIT

b = Student("Bbb", "Ccc", 4.0, "FOGI")
b.show()
# Output:
# Bbb - Ccc
# 4.0 - FOGI
```
