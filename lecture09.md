# Lecture 9: Databases I (PostgreSQL)

## Plan
- Connecting to a PostgreSQL database with `psycopg2`
- Creating tables
- Inserting data
- Updating data
- Querying data
- Deleting data

---

## 0. Setup

Install the `psycopg2` driver:

```bash
pip install psycopg2-binary
```

Start PostgreSQL and create a database:

```sql
CREATE DATABASE pp2_db;
```

---

## 1. Connect To PostgreSQL Database

`psycopg2` is the standard Python adapter for PostgreSQL.
A **connection** represents the session; a **cursor** executes SQL.

```python
import psycopg2

conn = psycopg2.connect(
    host="localhost",
    port=5432,
    dbname="pp2_db",
    user="postgres",
    password="secret"
)

cur = conn.cursor()
print("Connected:", conn.status)   # 1 = CONNECTION_OK

cur.close()
conn.close()
```

### Using a context manager (recommended)

```python
import psycopg2
from contextlib import closing

conn = psycopg2.connect(
    host="localhost",
    dbname="pp2_db",
    user="postgres",
    password="secret"
)

with conn:                      # auto commit/rollback
    with closing(conn.cursor()) as cur:
        cur.execute("SELECT version();")
        print(cur.fetchone()[0])

conn.close()
```

### Connection string format

```python
import psycopg2

# DSN string — alternative to keyword arguments
conn = psycopg2.connect("host=localhost dbname=pp2_db user=postgres password=secret")
```

---

## 2. Create Tables

### Basic syntax

```sql
CREATE TABLE table_name (
    column_name  DATA_TYPE  CONSTRAINTS,
    ...
);
```

### Common PostgreSQL data types

| Type | Description |
|------|-------------|
| `SERIAL` | Auto-incrementing integer (alias for sequence + integer) |
| `INTEGER` | Whole number |
| `VARCHAR(n)` | Variable-length string, max n chars |
| `TEXT` | Unlimited-length string |
| `FLOAT` | Floating-point number |
| `BOOLEAN` | `TRUE` / `FALSE` |
| `DATE` | Calendar date |
| `TIMESTAMP` | Date + time |

### Example

```python
import psycopg2

conn = psycopg2.connect(
    host="localhost", dbname="pp2_db",
    user="postgres", password="secret"
)
cur = conn.cursor()

# Create a students table
cur.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id         SERIAL       PRIMARY KEY,
        name       VARCHAR(100) NOT NULL,
        email      VARCHAR(100) UNIQUE NOT NULL,
        grade      FLOAT,
        enrolled   BOOLEAN      DEFAULT TRUE,
        created_at TIMESTAMP    DEFAULT CURRENT_TIMESTAMP
    );
""")

conn.commit()       # IMPORTANT: persist the changes
print("Table created.")

cur.close()
conn.close()
```

### Creating multiple related tables

```python
import psycopg2

conn = psycopg2.connect(
    host="localhost", dbname="pp2_db",
    user="postgres", password="secret"
)
cur = conn.cursor()

cur.execute("""
    CREATE TABLE IF NOT EXISTS courses (
        id    SERIAL       PRIMARY KEY,
        title VARCHAR(200) NOT NULL,
        code  VARCHAR(20)  UNIQUE NOT NULL
    );
""")

cur.execute("""
    CREATE TABLE IF NOT EXISTS enrollments (
        id         SERIAL  PRIMARY KEY,
        student_id INTEGER REFERENCES students(id) ON DELETE CASCADE,
        course_id  INTEGER REFERENCES courses(id)  ON DELETE CASCADE,
        score      FLOAT
    );
""")

conn.commit()
print("Tables created.")

cur.close()
conn.close()
```

### Task 1

Create a table called `books` with the following columns:
- `id` — auto-increment primary key
- `title` — required string, max 200 chars
- `author` — required string, max 100 chars
- `price` — float
- `in_stock` — boolean, default `TRUE`

**Solution:**

```python
import psycopg2

conn = psycopg2.connect(
    host="localhost", dbname="pp2_db",
    user="postgres", password="secret"
)
cur = conn.cursor()

cur.execute("""
    CREATE TABLE IF NOT EXISTS books (
        id       SERIAL       PRIMARY KEY,
        title    VARCHAR(200) NOT NULL,
        author   VARCHAR(100) NOT NULL,
        price    FLOAT,
        in_stock BOOLEAN      DEFAULT TRUE
    );
""")

conn.commit()
print("Table 'books' created.")

cur.close()
conn.close()
```

---

## 3. Insert Data Into Table

### Single row

```python
import psycopg2

conn = psycopg2.connect(
    host="localhost", dbname="pp2_db",
    user="postgres", password="secret"
)
cur = conn.cursor()

# Always use %s placeholders — NEVER format strings directly (SQL injection risk)
cur.execute(
    "INSERT INTO students (name, email, grade) VALUES (%s, %s, %s);",
    ("Alice", "alice@example.com", 90.5)
)

conn.commit()
print("Row inserted.")

cur.close()
conn.close()
```

### Retrieve the generated ID with `RETURNING`

```python
cur.execute(
    "INSERT INTO students (name, email, grade) VALUES (%s, %s, %s) RETURNING id;",
    ("Bob", "bob@example.com", 78.0)
)
new_id = cur.fetchone()[0]
conn.commit()
print(f"Inserted with id = {new_id}")
```

### Multiple rows with `executemany`

```python
import psycopg2

conn = psycopg2.connect(
    host="localhost", dbname="pp2_db",
    user="postgres", password="secret"
)
cur = conn.cursor()

students = [
    ("Charlie", "charlie@example.com", 85.0),
    ("Diana",   "diana@example.com",   92.5),
    ("Eve",     "eve@example.com",     60.0),
]

cur.executemany(
    "INSERT INTO students (name, email, grade) VALUES (%s, %s, %s);",
    students
)

conn.commit()
print(f"{cur.rowcount} rows inserted.")

cur.close()
conn.close()
```

### Task 2

Insert the following books into the `books` table using `executemany`:

| title | author | price |
|-------|--------|-------|
| Clean Code | Robert Martin | 35.99 |
| The Pragmatic Programmer | David Thomas | 42.00 |
| Python Crash Course | Eric Matthes | 29.99 |

**Solution:**

```python
import psycopg2

conn = psycopg2.connect(
    host="localhost", dbname="pp2_db",
    user="postgres", password="secret"
)
cur = conn.cursor()

books = [
    ("Clean Code",                "Robert Martin", 35.99),
    ("The Pragmatic Programmer",  "David Thomas",  42.00),
    ("Python Crash Course",       "Eric Matthes",  29.99),
]

cur.executemany(
    "INSERT INTO books (title, author, price) VALUES (%s, %s, %s);",
    books
)

conn.commit()
print(f"{cur.rowcount} books inserted.")

cur.close()
conn.close()
```

---

## 4. Update Data

### Basic UPDATE

```python
import psycopg2

conn = psycopg2.connect(
    host="localhost", dbname="pp2_db",
    user="postgres", password="secret"
)
cur = conn.cursor()

# Update a single student's grade
cur.execute(
    "UPDATE students SET grade = %s WHERE email = %s;",
    (95.0, "alice@example.com")
)

conn.commit()
print(f"Rows updated: {cur.rowcount}")

cur.close()
conn.close()
```

### Update multiple columns

```python
cur.execute(
    "UPDATE students SET grade = %s, enrolled = %s WHERE id = %s;",
    (88.0, False, 2)
)
conn.commit()
```

### Conditional bulk update

```python
# Give a 5-point bonus to everyone with grade < 70
cur.execute(
    "UPDATE students SET grade = grade + 5 WHERE grade < %s;",
    (70,)
)
conn.commit()
print(f"Students given bonus: {cur.rowcount}")
```

### Task 3

1. Set `in_stock = FALSE` for all books with `price > 40`.
2. Reduce the price of all books by 10%.

**Solution:**

```python
import psycopg2

conn = psycopg2.connect(
    host="localhost", dbname="pp2_db",
    user="postgres", password="secret"
)
cur = conn.cursor()

# 1. Mark expensive books as out of stock
cur.execute("UPDATE books SET in_stock = FALSE WHERE price > %s;", (40,))
print(f"Out of stock: {cur.rowcount}")

# 2. Apply 10% discount to all books
cur.execute("UPDATE books SET price = price * 0.9;")
print(f"Discounted: {cur.rowcount}")

conn.commit()
cur.close()
conn.close()
```

---

## 5. Query Data

### Fetch all rows — `fetchall()`

```python
import psycopg2

conn = psycopg2.connect(
    host="localhost", dbname="pp2_db",
    user="postgres", password="secret"
)
cur = conn.cursor()

cur.execute("SELECT id, name, grade FROM students;")
rows = cur.fetchall()       # list of tuples

for row in rows:
    print(row)              # (1, 'Alice', 95.0)

cur.close()
conn.close()
```

### Fetch one row — `fetchone()`

```python
cur.execute("SELECT * FROM students WHERE email = %s;", ("alice@example.com",))
row = cur.fetchone()
if row:
    print(row)
else:
    print("Not found.")
```

### Using column names with `RealDictCursor`

```python
import psycopg2
import psycopg2.extras

conn = psycopg2.connect(
    host="localhost", dbname="pp2_db",
    user="postgres", password="secret"
)
cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

cur.execute("SELECT * FROM students;")
for row in cur.fetchall():
    print(row["name"], row["grade"])    # access by column name

cur.close()
conn.close()
```

### Filtering, ordering, limiting

```python
import psycopg2

conn = psycopg2.connect(
    host="localhost", dbname="pp2_db",
    user="postgres", password="secret"
)
cur = conn.cursor()

# WHERE — filter rows
cur.execute("SELECT name, grade FROM students WHERE grade >= %s;", (85,))
print("High achievers:", cur.fetchall())

# ORDER BY — sort results
cur.execute("SELECT name, grade FROM students ORDER BY grade DESC;")
print("Ranked:", cur.fetchall())

# LIMIT and OFFSET — pagination
cur.execute("SELECT name FROM students ORDER BY name LIMIT %s OFFSET %s;", (2, 0))
print("Page 1:", cur.fetchall())

cur.close()
conn.close()
```

### Aggregate functions

```python
cur.execute("SELECT COUNT(*), AVG(grade), MAX(grade), MIN(grade) FROM students;")
count, avg, mx, mn = cur.fetchone()
print(f"Count={count}  Avg={avg:.1f}  Max={mx}  Min={mn}")
```

### Task 4

Query the `books` table and:
1. Print all books sorted by price ascending.
2. Print only books that are in stock.
3. Print the average price of all books.

**Solution:**

```python
import psycopg2

conn = psycopg2.connect(
    host="localhost", dbname="pp2_db",
    user="postgres", password="secret"
)
cur = conn.cursor()

# 1. All books sorted by price
cur.execute("SELECT title, author, price FROM books ORDER BY price ASC;")
print("All books:")
for title, author, price in cur.fetchall():
    print(f"  {title} by {author} — ${price:.2f}")

# 2. In-stock books only
cur.execute("SELECT title, price FROM books WHERE in_stock = TRUE;")
print("\nIn stock:")
for title, price in cur.fetchall():
    print(f"  {title} — ${price:.2f}")

# 3. Average price
cur.execute("SELECT AVG(price) FROM books;")
avg = cur.fetchone()[0]
print(f"\nAverage price: ${avg:.2f}")

cur.close()
conn.close()
```

### Task 5

Find all students whose name starts with a given letter using `LIKE`, and display them sorted by grade descending.

**Solution:**

```python
import psycopg2

conn = psycopg2.connect(
    host="localhost", dbname="pp2_db",
    user="postgres", password="secret"
)
cur = conn.cursor()

letter = "A"
cur.execute(
    "SELECT name, grade FROM students WHERE name LIKE %s ORDER BY grade DESC;",
    (letter + "%",)     # NEVER use f-string here!
)

for name, grade in cur.fetchall():
    print(f"{name}: {grade}")

cur.close()
conn.close()
```

---

## 6. Delete Data from Tables

### Delete specific rows

```python
import psycopg2

conn = psycopg2.connect(
    host="localhost", dbname="pp2_db",
    user="postgres", password="secret"
)
cur = conn.cursor()

cur.execute("DELETE FROM students WHERE email = %s;", ("eve@example.com",))
conn.commit()
print(f"Deleted: {cur.rowcount} row(s)")

cur.close()
conn.close()
```

### Delete with a condition

```python
# Delete all students who are not enrolled
cur.execute("DELETE FROM students WHERE enrolled = FALSE;")
conn.commit()
print(f"Removed unenrolled students: {cur.rowcount}")
```

### Delete all rows (keep table structure)

```python
# DELETE without WHERE removes every row
cur.execute("DELETE FROM students;")
conn.commit()

# Faster alternative: TRUNCATE (also resets SERIAL counter)
cur.execute("TRUNCATE TABLE students RESTART IDENTITY;")
conn.commit()
```

### Drop a table entirely

```python
cur.execute("DROP TABLE IF EXISTS books;")
conn.commit()
print("Table dropped.")
```

### Task 6

1. Delete all books that are out of stock (`in_stock = FALSE`).
2. Print how many books remain.

**Solution:**

```python
import psycopg2

conn = psycopg2.connect(
    host="localhost", dbname="pp2_db",
    user="postgres", password="secret"
)
cur = conn.cursor()

# 1. Delete out-of-stock books
cur.execute("DELETE FROM books WHERE in_stock = FALSE;")
deleted = cur.rowcount
conn.commit()
print(f"Deleted {deleted} book(s).")

# 2. Count remaining
cur.execute("SELECT COUNT(*) FROM books;")
remaining = cur.fetchone()[0]
print(f"Books remaining: {remaining}")

cur.close()
conn.close()
```

---

## Conclusion

### Key Takeaways

**Connecting:**
- `psycopg2.connect(host, dbname, user, password)` — opens a session
- Always call `conn.commit()` to persist changes (INSERT / UPDATE / DELETE)
- Use `with conn:` for automatic commit/rollback
- `cur.close()` and `conn.close()` to release resources

**Creating Tables:**
- `CREATE TABLE IF NOT EXISTS` — safe to run multiple times
- `SERIAL PRIMARY KEY` — auto-incrementing ID
- `NOT NULL`, `UNIQUE`, `DEFAULT`, `REFERENCES` — common constraints

**Inserting Data:**
- Single row: `cur.execute(sql, (val1, val2, ...))`
- Multiple rows: `cur.executemany(sql, list_of_tuples)`
- `RETURNING id` — get the auto-generated key back
- **Always use `%s` placeholders — never f-strings or `.format()` in SQL**

**Updating Data:**
- `UPDATE table SET col = %s WHERE condition;`
- `cur.rowcount` tells how many rows were affected

**Querying Data:**
- `cur.fetchone()` — single row as a tuple (or `None`)
- `cur.fetchall()` — all rows as a list of tuples
- `RealDictCursor` — access columns by name instead of index
- Filtering: `WHERE`, sorting: `ORDER BY`, pagination: `LIMIT / OFFSET`
- Aggregates: `COUNT`, `AVG`, `MAX`, `MIN`, `SUM`

**Deleting Data:**
- `DELETE FROM table WHERE condition;` — remove specific rows
- `DELETE FROM table;` — remove all rows (table stays)
- `TRUNCATE TABLE table RESTART IDENTITY;` — faster full wipe, resets counter
- `DROP TABLE IF EXISTS table;` — remove the table entirely

**Security:**
- Never concatenate user input into SQL strings → SQL injection
- Always pass parameters as the second argument to `execute()` / `executemany()`
