# Lecture 3: Functions, Lambda, and OOP

## Plan
- Functions
- Lambda functions
- Classes and objects
- Inheritance

---

## Functions

A **function** is a reusable block of code that performs a specific task. Functions help organize code, make it more readable, and follow the DRY (Don't Repeat Yourself) principle.

### Why Use Functions?
- **Reusability**: Write once, use many times
- **Modularity**: Break complex problems into smaller, manageable pieces
- **Readability**: Give meaningful names to blocks of code
- **Maintainability**: Fix bugs or make changes in one place

### Basic Function

Functions are defined using the `def` keyword, followed by the function name and parentheses.

```python
def func():
    print("Hello!")

func()
```

### Functions with Arguments

**Parameters** are variables listed in the function definition. **Arguments** are actual values passed to the function when calling it.

Python supports different ways to pass arguments:
- **Positional arguments**: Values are assigned based on their position
- **Keyword arguments**: Values are assigned by parameter name

```python
def func(arg1, arg2):
    print(arg1 + arg2)

func(3, 5)
func(arg1 = "hello ", arg2 = "all")
func([1, 2, 3], [4, 5, 6])
```

### Modifying Mutable Arguments

In Python, arguments are passed by **object reference**. For mutable objects (lists, dictionaries), changes inside the function affect the original object.

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

The `*args` syntax allows a function to accept any number of positional arguments. Inside the function, `args` is a tuple containing all passed values.

```python
def func(a, *args):
    for arg in args:
        print(arg, type(arg))

func([1, 2, 3], "hello", 10)
func(1, 2, 3, 4, 5)
```

### Using *args for Sum

A practical example of `*args` - creating a flexible sum function:

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

The `return` statement sends a value back to the caller. Functions without `return` (or with just `return`) return `None`.

```python
def func1(num1, num2):
    print(num1 + num2)

def func2(num1, num2):
    return num1 + num2

print(func1(3, 5))  # None - func1 does not return anything
print(func2(3, 5))  # 8
```

### Default Parameter Values

Default values make parameters optional. If no argument is provided, the default value is used.

**Important**: Default parameters must come after non-default parameters.

```python
def func(num1 = 0, num2 = 0):
    print(num1 + num2)

func()       # 0
func(3)      # 3
func(3, 5)   # 8
```

### **kwargs (Variable Keyword Arguments)

The `**kwargs` syntax allows a function to accept any number of keyword arguments. Inside the function, `kwargs` is a dictionary.

```python
def func(**kwargs):
    print(kwargs)  # kwargs is a dict
    for key in kwargs:
        print(key, kwargs[key])

func(fname = "Askar", lname = "Akshabayev")
```

### Variable Scope

**Scope** determines where a variable can be accessed. Python has two main scopes:
- **Global scope**: Variables defined outside functions, accessible everywhere
- **Local scope**: Variables defined inside functions, accessible only within that function

### Global Variables

Variables defined outside functions are global and can be read inside functions:

```python
x = 1  # global variable

def func():
    print(x)

func()
```

### Local Variables

Variables defined inside a function are local and shadow global variables with the same name:

```python
x = 1  # global variable

def func():
    x = 2  # local variable (different from global x)
    print(x)

func()  # prints 2
print(x)  # prints 1 (global x unchanged)
```

### Using `global` Keyword

To modify a global variable inside a function, use the `global` keyword:

```python
x = 1  # global variable

def func():
    global x  # allows to modify x within a function
    x += 1
    print(x)

func()
print(x)  # x is now 2
```

**Note**: Overusing `global` is considered bad practice. Prefer passing values as arguments and returning results.

### Finding Maximum Value

Functions can contain conditional logic to make decisions:

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

Python functions can return multiple values as a tuple. You can unpack them into separate variables:

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

The underscore `_` is a convention for variables you don't need.

### Recursion with Memoization

**Recursion** is when a function calls itself. **Memoization** is an optimization technique that stores results of expensive function calls.

This example calculates Fibonacci numbers efficiently:

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

Without memoization, recursive Fibonacci has exponential time complexity O(2^n). With memoization, it becomes linear O(n).

---

## Lambda Functions

**Lambda functions** (also called anonymous functions) are small, single-expression functions defined using the `lambda` keyword.

### Syntax
```
lambda arguments: expression
```

### When to Use Lambda Functions?
- Short, simple operations that don't need a full function definition
- As arguments to higher-order functions like `map()`, `filter()`, `sorted()`
- When a function is used only once

### Basic Lambda

```python
def my_power(x, y):
    return x ** y
```

This is equivalent to:
```python
my_power = lambda x, y: x ** y
print(my_power(2, 3))  # 8
```

### map() with Lambda

The `map()` function applies a function to every item in an iterable (list, tuple, etc.) and returns a map object.

**Syntax**: `map(function, iterable)`

```python
nums = [48, 6, 9, 21, 1]
square_all = map(lambda num: num ** 2, nums)
print(list(square_all))  # [2304, 36, 81, 441, 1]
```

### Function Returning Lambda (Closures)

Functions can return lambda functions. This creates a **closure** - a function that remembers values from its enclosing scope.

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

The `filter()` function creates an iterator of elements for which a function returns `True`.

**Syntax**: `filter(function, iterable)`

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

**Object-Oriented Programming (OOP)** is a programming paradigm based on the concept of "objects" that contain data (attributes) and code (methods).

### Core OOP Concepts

| Concept | Description |
|---------|-------------|
| **Class** | A blueprint/template for creating objects |
| **Object** | An instance of a class |
| **Attribute** | Data stored inside an object (variables) |
| **Method** | Functions that belong to an object |
| **Inheritance** | Mechanism to create a new class from an existing class |
| **Encapsulation** | Bundling data and methods that operate on that data |

### Why Use OOP?
- **Organization**: Group related data and functions together
- **Reusability**: Inherit and extend existing classes
- **Modularity**: Each object is independent and can be modified without affecting others
- **Real-world modeling**: Objects can represent real-world entities

### Basic Class

Classes are defined using the `class` keyword. By convention, class names use CamelCase.

```python
class MyClass:
    # fields (class attributes)
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

### The `self` Parameter

`self` refers to the current instance of the class. It must be the first parameter of every method (though you don't pass it when calling).

### The `__init__` Method (Constructor)

The `__init__` method is called automatically when creating a new object. It's used to initialize object attributes.

### Inheritance

**Inheritance** allows a class (child/subclass) to inherit attributes and methods from another class (parent/superclass).

Benefits of inheritance:
- **Code reuse**: Don't repeat code that's already in the parent class
- **Extensibility**: Add new features to child classes
- **Polymorphism**: Child classes can override parent methods

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

### The `super()` Function

`super()` returns a proxy object that allows you to call methods from the parent class. This is essential for:
- Calling the parent's `__init__` to initialize inherited attributes
- Extending (not replacing) parent methods

---

## Conclusion

### Key Takeaways

**Functions**:
- Functions are reusable blocks of code defined with `def`
- Parameters can have default values, making them optional
- `*args` collects extra positional arguments into a tuple
- `**kwargs` collects extra keyword arguments into a dictionary
- Functions can return multiple values using tuples
- Use `global` keyword carefully to modify global variables inside functions
- Recursion with memoization can dramatically improve performance

**Lambda Functions**:
- Lambda functions are concise, single-expression functions
- Syntax: `lambda arguments: expression`
- Commonly used with `map()`, `filter()`, and `sorted()`
- Best for simple operations; use regular functions for complex logic

**OOP**:
- Classes are blueprints for creating objects
- Objects have attributes (data) and methods (behavior)
- `__init__` is the constructor method, called when creating objects
- `self` refers to the current instance
- Inheritance allows classes to inherit from other classes
- `super()` is used to call parent class methods
