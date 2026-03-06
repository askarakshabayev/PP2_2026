# Lecture 6: Regular Expressions

## Plan
- Introduction to Regex
- Matching, searching, replacing (`match`, `fullmatch`, `search`, `findall`, `finditer`, `split`, `sub`)
- Metacharacters
- Quantifiers
- Special sequences
- Character classes
- Groups and capture groups
- `re.compile()` and efficient pattern usage
- Practical example: extracting data from real text

---

## 1. Introduction to Regex

A **regular expression** (regex) is a sequence of characters that defines a search pattern. Python's built-in `re` module provides full support for regular expressions.

Use cases:
- Validating emails, phone numbers, passwords
- Extracting data from text
- Searching and replacing in strings

```python
import re

text = "Hello, my email is student@kbtu.kz"
pattern = r"\w+@\w+\.\w+"

match = re.search(pattern, text)
print(match.group())  # student@kbtu.kz
```

> **Note:** Always use raw strings (`r"..."`) for regex patterns to avoid issues with backslashes.

### Common Patterns Reference

| Pattern | Meaning | Example match |
|---------|---------|---------------|
| `\d{5}` | Exactly 5 digits | `12345` |
| `\d\d/\d\d/\d{4}` | Date ДД/ММ/ГГГГ | `25/02/2026` |
| `\b\w{3}\b` | Exactly 3-letter word | `cat`, `the` |
| `[-+]?\d+` | Integer (with optional sign) | `42`, `-7`, `+100` |
| `\d+\.\d+` | Decimal number | `18.81`, `3.14` |
| `\w+@\w+\.\w{2,4}` | Simple email | `user@mail.com` |
| `(\+7\|8)\(?\d{3}\)?-?\d{3}-\d{2}-\d{2}` | KZ phone number | `+7(707)123-11-22` |

> **Equivalents:** `\d{1,}` = `\d+`  •  `\d{0,}` = `\d*`  •  `\d{0,1}` = `\d?`  •  `[A-Za-z0-9_]` = `\w`

---

## 2. Matching, Searching, Replacing

The `re` module provides several key functions:

| Function | Description |
|----------|-------------|
| `re.search()` | Searches for the **first occurrence** anywhere in the string |
| `re.match()` | Matches pattern **at the beginning** of the string |
| `re.fullmatch()` | Checks if the **entire** string matches the pattern |
| `re.findall()` | Returns a **list** of all matches |
| `re.finditer()` | Returns an **iterator** of match objects (with positions) |
| `re.split()` | Splits string by pattern (like `str.split()` but with regex) |
| `re.sub()` | **Replaces** matches with a given string |

### `re.match()` — matches at the start

```python
import re

result = re.match(r"Hello", "Hello, World!")
print(result.group())  # Hello

result = re.match(r"World", "Hello, World!")
print(result)  # None  (doesn't start with "World")
```

### `re.search()` — finds first match anywhere

```python
import re

result = re.search(r"World", "Hello, World!")
print(result.group())   # World
print(result.start())   # 7  (index where match starts)
print(result.end())     # 12 (index where match ends)
```

### `re.fullmatch()` — entire string must match

```python
import re

# fullmatch checks the WHOLE string, not just a part of it
print(re.fullmatch(r'\d\d\D\d\d', '12-12'))     # match  -> YES
print(re.fullmatch(r'\d\d\D\d\d', 'Т. 12-12'))  # None   -> NO

def validate(pattern, value):
    return 'YES' if re.fullmatch(pattern, value) else 'NO'

print(validate(r'[a-z]+', 'hello'))    # YES
print(validate(r'[a-z]+', 'Hello'))    # NO  (has uppercase)
print(validate(r'\d{4}', '2026'))      # YES
print(validate(r'\d{4}', '26'))        # NO  (not exactly 4 digits)
```

### `re.findall()` — returns all matches

```python
import re

text = "cat bat sat mat"
matches = re.findall(r"\bat\b", text)
print(matches)  # []  — "at" alone doesn't appear

matches = re.findall(r"\w+at", text)
print(matches)  # ['cat', 'bat', 'sat', 'mat']

# Find all dates in text
text2 = 'Written on 19.01.2018, updated on 01.09.2024'
print(re.findall(r'\d\d\.\d\d\.\d{4}', text2))
# ['19.01.2018', '01.09.2024']
```

### `re.finditer()` — iterator with match positions

```python
import re

text = 'Written on 19.01.2018, updated on 01.09.2024'
for m in re.finditer(r'\d\d\.\d\d\.\d{4}', text):
    print(f'Date {m[0]} starts at position {m.start()}')
# Date 19.01.2018 starts at position 11
# Date 01.09.2024 starts at position 34
```

### `re.split()` — split by pattern

```python
import re

txt = "The          rain     in      Spain"

# Split by any whitespace sequence
print(re.split(r'\s+', txt))
# ['The', 'rain', 'in', 'Spain']

# Split by non-word characters (punctuation, spaces, etc.)
print(re.split(r'\W+', 'Where, please tell me, my glasses??!'))
# ['Where', 'please', 'tell', 'me', 'my', 'glasses', '']
```

### `re.sub()` — replace matches

```python
import re

text = "I love cats. Cats are great. My cat is named Whiskers."
result = re.sub(r"[Cc]at", "dog", text)
print(result)
# I love dogs. dogs are great. My dog is named Whiskers.

# Limit replacements with count parameter
result = re.sub(r"[Cc]at", "dog", text, count=1)
print(result)
# I love dogs. Cats are great. My cat is named Whiskers.
```

### Task 1

Given the string `"Phone: +7-777-123-45-67, backup: +7-701-987-65-43"`, extract all phone numbers and print them as a list.

**Solution:**

```python
import re

text = "Phone: +7-777-123-45-67, backup: +7-701-987-65-43"
phones = re.findall(r"\+7-\d{3}-\d{3}-\d{2}-\d{2}", text)
print(phones)
# ['+7-777-123-45-67', '+7-701-987-65-43']
# r"(\+7|8)-?(\d{3})-?(\d{3})-?(\d{2})-?(\d{2})"
```

---

## 3. Metacharacters

**Metacharacters** are characters with special meaning in regex.

| Metacharacter | Meaning | Example | Matches |
|---------------|---------|---------|---------|
| `.` | Any character except newline | `a.c` | `abc`, `a1c`, `a c` |
| `^` | Start of string | `^Hello` | `Hello world` |
| `$` | End of string | `world$` | `Hello world` |
| `|` | OR | `cat|dog` | `cat` or `dog` |
| `()` | Group | `(ab)+` | `ab`, `abab` |
| `\` | Escape special character | `\.` | literal `.` |

### Examples

```python
import re

# . matches any single character
print(re.findall(r"c.t", "cat cut c@t c  t"))  # ['cat', 'cut', 'c@t']

# ^ and $ — anchors
print(re.search(r"^Python", "Python is fun"))   # matches
print(re.search(r"^Python", "I love Python"))   # None

print(re.search(r"fun$", "Python is fun"))      # matches
print(re.search(r"fun$", "fun times ahead"))    # None

# | — alternation
print(re.findall(r"cat|dog", "I have a cat and a dog"))
# ['cat', 'dog']

# Escaping a dot
print(re.findall(r"3\.14", "pi is 3.14 not 3X14"))  # ['3.14']
```

### Task 2

Check if a string starts with `"Error"` and ends with `"!"`. Print `True` or `False`.

**Solution:**

```python
import re

def is_error_message(text):
    return bool(re.match(r"^Error.*!$", text))

print(is_error_message("Error: file not found!"))  # True
print(is_error_message("Error: connection lost"))  # False
print(is_error_message("Warning: disk full!"))     # False
```

---

## 4. Quantifiers

**Quantifiers** define how many times a character or group must appear.

| Quantifier | Meaning |
|------------|---------|
| `*` | 0 or more |
| `+` | 1 or more |
| `?` | 0 or 1 (optional) |
| `{n}` | Exactly n times |
| `{n,}` | n or more times |
| `{n,m}` | Between n and m times |

### Examples

```python
import re

text = "colour color colouur"

# * — zero or more 'u'
print(re.findall(r"colou*r", text))   # ['colour', 'color', 'colouur']

# + — one or more 'u'
print(re.findall(r"colou+r", text))   # ['colour', 'colouur']

# ? — zero or one 'u'
print(re.findall(r"colou?r", text))   # ['colour', 'color']

# {n} — exactly n digits
print(re.findall(r"\d{4}", "Year: 2026, Code: 42, ID: 1234"))
# ['2026', '1234']

# {n,m} — between n and m digits
print(re.findall(r"\d{2,4}", "1 22 333 4444 55555"))
# ['22', '333', '4444', '5555']
```

### Greedy vs Lazy

By default, quantifiers are **greedy** — they match as much as possible. Add `?` to make them **lazy** (match as little as possible).

```python
import re

html = "<b>bold</b> and <i>italic</i>"

# Greedy — matches everything between first < and last >
print(re.findall(r"<.+>", html))
# ['<b>bold</b> and <i>italic</i>']

# Lazy — matches the shortest possible string
print(re.findall(r"<.+?>", html))
# ['<b>', '</b>', '<i>', '</i>']
```

### Task 3

Validate a password: it must be **at least 8 characters** and contain **at least one digit**. Print `"Valid"` or `"Invalid"`.

**Solution:**

```python
import re

def check_password(password):
    has_length = len(password) >= 8
    has_digit = bool(re.search(r"\d", password))
    return "Valid" if has_length and has_digit else "Invalid"

print(check_password("abc123"))       # Invalid (too short)
print(check_password("abcdefgh"))     # Invalid (no digit)
print(check_password("abcdef12"))     # Valid
```

---

## 5. Special Sequences

Special sequences are shorthand for common character patterns.

| Sequence | Matches |
|----------|---------|
| `\d` | Any digit `[0-9]` |
| `\D` | Any non-digit |
| `\w` | Any word character `[a-zA-Z0-9_]` |
| `\W` | Any non-word character |
| `\s` | Any whitespace (space, tab, newline) |
| `\S` | Any non-whitespace |
| `\b` | Word boundary |
| `\B` | Non-word boundary |

### Examples

```python
import re

text = "User: alice_99, Age: 20, Score: 95.5"

# \d+ — extract all numbers
print(re.findall(r"\d+", text))
# ['99', '20', '95', '5']

# \d+\.?\d* — extract decimals too
print(re.findall(r"\d+\.?\d*", text))
# ['99', '20', '95.5']

# \w+ — extract all words/identifiers
print(re.findall(r"\w+", text))
# ['User', 'alice_99', 'Age', '20', 'Score', '95', '5']

# \s+ — split on whitespace
print(re.split(r"\s+", "hello   world\tfoo\nbar"))
# ['hello', 'world', 'foo', 'bar']

# \b — whole word boundary
print(re.findall(r"\bcat\b", "cat concatenate scatter cat"))
# ['cat', 'cat']
```

### Task 4

Given the text below, extract only **whole words that start with a capital letter**.

```
text = "Alice went to Almaty. she met Bob and carol there."
```

**Solution:**

```python
import re

text = "Alice went to Almaty. she met Bob and carol there."
capitalized = re.findall(r"\b[A-Z][a-z]*\b", text)
print(capitalized)
# ['Alice', 'Almaty', 'Bob']
```

---

## 6. Character Classes

**Character classes** `[...]` match any one character from the set.

| Pattern | Matches |
|---------|---------|
| `[abc]` | `a`, `b`, or `c` |
| `[^abc]` | Any character except `a`, `b`, `c` |
| `[a-z]` | Any lowercase letter |
| `[A-Z]` | Any uppercase letter |
| `[0-9]` | Any digit (same as `\d`) |
| `[a-zA-Z0-9]` | Any alphanumeric character |

### Examples

```python
import re

# Match vowels
print(re.findall(r"[aeiou]", "Hello World"))
# ['e', 'o', 'o']

# Match consonants (not vowels, not space/punct)
print(re.findall(r"[^aeiou\s\W]", "Hello World"))
# ['H', 'l', 'l', 'W', 'r', 'l', 'd']

# Match hex digits
print(re.findall(r"[0-9A-Fa-f]+", "Color: #1aF3c9 or #FFFFFF"))
# ['1aF3c9', 'FFFFFF']

# Match Kazakhstan mobile numbers format: +7 (7XX) XXX-XX-XX
text = "Call +7 (701) 123-45-67 or +7 (777) 987-65-43"
pattern = r"\+7 \(7\d{2}\) \d{3}-\d{2}-\d{2}"
print(re.findall(pattern, text))
# ['+7 (701) 123-45-67', '+7 (777) 987-65-43']
```

### Task 5

Write a function that removes all characters from a string **except letters and spaces**.

**Solution:**

```python
import re

def letters_only(text):
    return re.sub(r"[^a-zA-Z ]", "", text)

print(letters_only("H3ll0 W0rld!"))    # Hll Wrld
print(letters_only("P@ssw0rd#123"))    # Psswrd
print(letters_only("Hello, World!"))   # Hello World
```

### Task 6

Validate an email address. A valid email: `word@word.domain` where domain is 2–4 letters.

**Solution:**

```python
import re

def validate_email(email):
    pattern = r"^[\w.-]+@[\w.-]+\.[a-zA-Z]{2,4}$"
    return bool(re.match(pattern, email))

print(validate_email("student@kbtu.kz"))    # True
print(validate_email("user.name@mail.com")) # True
print(validate_email("bad@email"))          # False
print(validate_email("@nodomain.com"))      # False
```

---

## 7. Groups

**Groups** `()` let you capture specific parts of a match. You can access them by index or by name.

```python
import re

# Numbered groups — group(0) is the full match, group(1) is the first ()
txt = 'The rain in Spain 1234'

x = re.search(r'(.+)(\b[0-9]+)', txt)
print(x.group(0))    # The rain in Spain 1234  (full match)
print(x.group(1))    # The rain in Spain       (first group)
print(x.group(2))    # 1234                    (second group)
print(x.groups())    # ('The rain in Spain ', '1234')
```

### Named Groups `(?P<name>...)`

Named groups make patterns easier to read and access by meaningful names instead of indices.

```python
import re

# Parse a date string into parts
pattern = re.compile(r'(?P<day>\d{2})\.(?P<month>\d{2})\.(?P<year>\d{4})')
text = 'Written on 19.01.2018, updated on 01.09.2024'

for m in pattern.finditer(text):
    print(f"Day: {m.group('day')}, Month: {m.group('month')}, Year: {m.group('year')}")
# Day: 19, Month: 01, Year: 2018
# Day: 01, Month: 09, Year: 2024
```

### Task 9

Parse phone numbers from text and extract the **operator code** and **number** separately.

```
text = "Call me: +7(707)123-11-22 or +7(701)987-65-43"
```

**Solution:**

```python
import re

text = "Call me: +7(707)123-11-22 or +7(701)987-65-43"
pattern = re.compile(r'\+7\((?P<code>\d{3})\)(?P<number>\d{3}-\d{2}-\d{2})')

for m in pattern.finditer(text):
    print(f"Code: {m.group('code')}, Number: {m.group('number')}")
# Code: 707, Number: 123-11-22
# Code: 701, Number: 987-65-43
```

---

## 8. `re.compile()` and Efficient Pattern Usage

When you use the same pattern multiple times, it's more efficient to **compile** it once with `re.compile()`. This avoids re-parsing the pattern on every call.

```python
import re

# Without compile — pattern is parsed every time
for name in ["Alice", "Bob", "Charlie"]:
    if re.match(r"^[A-Z][a-z]+$", name):
        print(f"{name} is valid")

# With compile — pattern parsed only once
name_pattern = re.compile(r"^[A-Z][a-z]+$")
for name in ["Alice", "Bob", "charlie", "DAVE"]:
    if name_pattern.match(name):
        print(f"{name} is valid")
    else:
        print(f"{name} is invalid")
# Alice is valid
# Bob is valid
# charlie is invalid
# DAVE is invalid
```

SELF STUDY
### Flags

Flags modify how the pattern is applied.

| Flag | Short | Meaning |
|------|-------|---------|
| `re.IGNORECASE` | `re.I` | Case-insensitive matching |
| `re.MULTILINE` | `re.M` | `^` and `$` match each line |
| `re.DOTALL` | `re.S` | `.` matches newline too |

```python
import re

# re.IGNORECASE
pattern = re.compile(r"python", re.IGNORECASE)
print(pattern.findall("Python PYTHON python PyThOn"))
# ['Python', 'PYTHON', 'python', 'PyThOn']

# re.MULTILINE
text = "first line\nsecond line\nthird line"
pattern = re.compile(r"^\w+", re.MULTILINE)
print(pattern.findall(text))
# ['first', 'second', 'third']

# re.DOTALL — . matches newline
text = "<div>\n  Hello\n</div>"
pattern = re.compile(r"<div>(.+?)</div>", re.DOTALL)
match = pattern.search(text)
print(match.group(1).strip())  # Hello
```

### Groups with `re.compile()`

Parentheses `()` create **capture groups** to extract specific parts of a match.

```python
import re

# Named groups with (?P<name>...)
pattern = re.compile(r"(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})")

dates = ["2026-02-25", "1999-12-31", "2000-01-01"]
for date in dates:
    m = pattern.match(date)
    if m:
        print(f"Year: {m.group('year')}, Month: {m.group('month')}, Day: {m.group('day')}")
# Year: 2026, Month: 02, Day: 25
# Year: 1999, Month: 12, Day: 31
# Year: 2000, Month: 01, Day: 01
```

### Task 7

Compile a pattern to find all words that appear **more than once** in a sentence. Print each duplicate word.

**Solution:**

```python
import re
from collections import Counter

text = "the cat sat on the mat and the cat sat again"

word_pattern = re.compile(r"\b\w+\b")
words = word_pattern.findall(text.lower())
counts = Counter(words)

duplicates = [word for word, count in counts.items() if count > 1]
print(duplicates)
# ['the', 'cat', 'sat']
```

### Task 8

Write a log parser using `re.compile()`. Given log lines like:
```
[2026-02-25 10:30:01] ERROR: Disk full
[2026-02-25 10:31:05] INFO: Backup started
[2026-02-25 10:32:44] ERROR: Connection timeout
```
Extract and print only **ERROR** entries with their timestamp and message.

**Solution:**

```python
import re

log = """[2026-02-25 10:30:01] ERROR: Disk full
[2026-02-25 10:31:05] INFO: Backup started
[2026-02-25 10:32:44] ERROR: Connection timeout"""

pattern = re.compile(
    r"\[(?P<timestamp>[\d\- :]+)\] ERROR: (?P<message>.+)"
)

for line in log.splitlines():
    m = pattern.search(line)
    if m:
        print(f"Time: {m.group('timestamp')} | Error: {m.group('message')}")
# Time: 2026-02-25 10:30:01 | Error: Disk full
# Time: 2026-02-25 10:32:44 | Error: Connection timeout
```

---

## 9. Practical Example: Extracting Data from Real Text

The real power of regex becomes clear when working with messy real-world text. Below is a rich text with emails, dates, times, phone numbers, and numbers — let's extract each type.

```python
import re

text = """
asd@gmail.com
Asd2213@mail.ru
asd3_asd@gmail.com
bobur.mukhsimbaev@kbtu.kz

20.02.2021  14:56:10
20.02.2024  09:30:00

+7707-123-11-22
+7(707)123-11-22
8(707)123-11-22

Kazakhstan has a land area of 22,724,900 square kilometres.
Population: 18.81 million. Density: fewer than 6 people per sq km.
It has [four][4][13123] official sources.
"""

# 1. Emails (letters, digits, _ allowed; only simple domains)
emails = re.findall(r'[a-z0-9_.]+@[a-z]+\.[a-z]{2,4}', text, re.IGNORECASE)
print("Emails:", emails)
# ['asd@gmail.com', 'Asd2213@mail.ru', 'asd3_asd@gmail.com', 'bobur.mukhsimbaev@kbtu.kz']

# 2. Dates in format DD.MM.YYYY
dates = re.findall(r'\d{2}\.\d{2}\.\d{4}', text)
print("Dates:", dates)
# ['20.02.2021', '20.02.2024']

# 3. Times in format HH:MM:SS
times = re.findall(r'\d{2}:\d{2}:\d{2}', text)
print("Times:", times)
# ['14:56:10', '09:30:00']

# 4. Phone numbers: +7XXX-XXX-XX-XX or +7(XXX)XXX-XX-XX or 8(XXX)XXX-XX-XX
phones = re.findall(r'(\+7|8)\(?\d{3}\)?-?\d{3}-\d{2}-\d{2}', text)
print("Phones:", phones)
# ['+7', '+7', '8']  — phones is list of groups; use full match:
phones = re.findall(r'(?:\+7|8)\(?\d{3}\)?-?\d{3}-\d{2}-\d{2}', text)
print("Phones:", phones)
# ['+7707-123-11-22', '+7(707)123-11-22', '8(707)123-11-22']

# 5. Numbers with comma separators: 22,724,900
big_numbers = re.findall(r'\d+(?:,\d{3})+', text)
print("Big numbers:", big_numbers)
# ['22,724,900']

# 6. Decimal numbers
decimals = re.findall(r'\d+\.\d+', text)
print("Decimals:", decimals)
# ['18.81']

# 7. Content inside square brackets [...]
bracketed = re.findall(r'\[\w+\]', text)
print("Bracketed:", bracketed)
# ['[four]', '[4]', '[13123]']
```

### Task 10

From the text above, build a summary dictionary with counts of each type found.

**Solution:**

```python
import re

text = """
asd@gmail.com Asd2213@mail.ru asd3_asd@gmail.com bobur.mukhsimbaev@kbtu.kz
20.02.2021  14:56:10   20.02.2024  09:30:00
+7707-123-11-22  +7(707)123-11-22  8(707)123-11-22
Kazakhstan has 22,724,900 sq km. Population: 18.81 million.
[four][4][13123]
"""

summary = {
    "emails":      re.findall(r'[a-z0-9_.]+@[a-z]+\.[a-z]{2,4}', text, re.I),
    "dates":       re.findall(r'\d{2}\.\d{2}\.\d{4}', text),
    "times":       re.findall(r'\d{2}:\d{2}:\d{2}', text),
    "phones":      re.findall(r'(?:\+7|8)\(?\d{3}\)?-?\d{3}-\d{2}-\d{2}', text),
    "big_numbers": re.findall(r'\d+(?:,\d{3})+', text),
    "decimals":    re.findall(r'\d+\.\d+', text),
    "bracketed":   re.findall(r'\[\w+\]', text),
}

for key, values in summary.items():
    print(f"{key:12}: {len(values)} found -> {values}")
```

---

## Conclusion

### Key Takeaways

**Introduction to Regex**:
- Import the `re` module to use regular expressions in Python
- Always use raw strings (`r"..."`) for patterns to avoid backslash issues

**Matching, Searching, Replacing**:
- `re.match()` — checks only at the start of the string
- `re.fullmatch()` — the entire string must match the pattern
- `re.search()` — finds first match anywhere in the string
- `re.findall()` — returns all matches as a list
- `re.finditer()` — iterator of match objects with positions (`m.start()`, `m.group()`)
- `re.split()` — splits string by a regex pattern
- `re.sub()` — replaces matches with a specified string

**Groups**:
- `()` creates a numbered capture group; `group(0)` = full match, `group(1)` = first group
- `(?P<name>...)` creates a named group, accessible via `m.group('name')`
- `.groups()` returns all captured groups as a tuple

**Metacharacters**:
- `.` matches any character; `^` and `$` anchor to start/end
- `|` for alternation; `()` for grouping; `\` to escape

**Quantifiers**:
- `*`, `+`, `?` control repetition; `{n,m}` for exact ranges
- Add `?` after a quantifier to make it lazy (e.g., `+?`)

**Special Sequences**:
- `\d` = digit, `\w` = word char, `\s` = whitespace
- `\b` = word boundary for whole-word matching

**Character Classes**:
- `[abc]` matches one of the listed characters
- `[^abc]` matches anything NOT in the set
- `[a-z]`, `[0-9]` define ranges

**`re.compile()`**:
- Compile once, reuse many times for better performance
- Use flags like `re.IGNORECASE`, `re.MULTILINE`, `re.DOTALL`
- Named groups `(?P<name>...)` make matches readable and maintainable
