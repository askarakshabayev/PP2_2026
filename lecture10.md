# Lecture 10: Databases II (PostgreSQL Advanced)

## Plan
- Handle Transactions
- Call PostgreSQL Functions
- Call PostgreSQL Stored Procedures
- Work with BLOB Data

---

## 0. Setup

Reuse the database from Lecture 9. Create a sample schema for examples:

```sql
CREATE TABLE IF NOT EXISTS parts (
    part_id   SERIAL       PRIMARY KEY,
    part_name VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS vendors (
    vendor_id   SERIAL       PRIMARY KEY,
    vendor_name VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS part_vendors (
    part_id   INTEGER REFERENCES parts(part_id),
    vendor_id INTEGER REFERENCES vendors(vendor_id),
    PRIMARY KEY (part_id, vendor_id)
);

CREATE TABLE IF NOT EXISTS part_drawings (
    part_id        INTEGER REFERENCES parts(part_id),
    file_extension VARCHAR(5),
    drawing_data   BYTEA
);
```

---

## 1. Handle Transactions

A **transaction** is a group of SQL statements that are executed as a single unit.
Either all changes succeed and are committed, or all are rolled back on failure.

### How psycopg2 manages transactions

- When you execute the **first SQL statement**, psycopg2 automatically begins a transaction.
- `conn.commit()` — permanently saves all changes made since the last commit.
- `conn.rollback()` — discards all changes and returns to the previous state.

### Basic pattern: try / except

```python
import psycopg2

conn = psycopg2.connect(
    host="localhost", dbname="pp2_db",
    user="postgres", password="secret"
)
cur = conn.cursor()

try:
    # Insert a new part
    cur.execute(
        "INSERT INTO parts (part_name) VALUES (%s) RETURNING part_id;",
        ("Bolt M8",)
    )
    part_id = cur.fetchone()[0]

    # Insert a vendor
    cur.execute(
        "INSERT INTO vendors (vendor_name) VALUES (%s) RETURNING vendor_id;",
        ("Steel Corp",)
    )
    vendor_id = cur.fetchone()[0]

    # Link part to vendor
    cur.execute(
        "INSERT INTO part_vendors (part_id, vendor_id) VALUES (%s, %s);",
        (part_id, vendor_id)
    )

    conn.commit()
    print(f"Transaction committed. part_id={part_id}, vendor_id={vendor_id}")

except Exception as e:
    conn.rollback()
    print(f"Transaction rolled back: {e}")

finally:
    cur.close()
    conn.close()
```

### Context manager pattern (recommended)

The `with conn:` block automatically calls `commit()` on success and `rollback()` on exception.

```python
import psycopg2

conn = psycopg2.connect(
    host="localhost", dbname="pp2_db",
    user="postgres", password="secret"
)

try:
    with conn:                      # auto commit / rollback
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO parts (part_name) VALUES (%s) RETURNING part_id;",
                ("Nut M8",)
            )
            part_id = cur.fetchone()[0]

            cur.execute(
                "INSERT INTO vendors (vendor_name) VALUES (%s) RETURNING vendor_id;",
                ("Fasteners Ltd",)
            )
            vendor_id = cur.fetchone()[0]

            cur.execute(
                "INSERT INTO part_vendors (part_id, vendor_id) VALUES (%s, %s);",
                (part_id, vendor_id)
            )
    print("Transaction committed.")
except Exception as e:
    print(f"Transaction rolled back: {e}")
finally:
    conn.close()
```

### Autocommit mode

Setting `autocommit = True` makes every statement execute and commit immediately.
Use this for DDL statements like `CREATE DATABASE` or `VACUUM` that cannot run inside a transaction.

```python
import psycopg2

conn = psycopg2.connect(
    host="localhost", dbname="pp2_db",
    user="postgres", password="secret"
)
conn.autocommit = True          # each statement commits automatically

with conn.cursor() as cur:
    cur.execute("VACUUM ANALYZE parts;")
    print("VACUUM completed.")

conn.close()
```

### Task 1

Write a function `transfer_vendor(part_name, old_vendor, new_vendor)` that:
1. Looks up (or inserts) the part and both vendors by name.
2. Removes the link between the part and `old_vendor`.
3. Creates a link between the part and `new_vendor`.
4. Wraps everything in a single transaction — if any step fails, roll back all changes.

**Solution:**

```python
import psycopg2

def get_or_create(cur, table, name_col, name_val, id_col):
    cur.execute(f"SELECT {id_col} FROM {table} WHERE {name_col} = %s;", (name_val,))
    row = cur.fetchone()
    if row:
        return row[0]
    cur.execute(
        f"INSERT INTO {table} ({name_col}) VALUES (%s) RETURNING {id_col};",
        (name_val,)
    )
    return cur.fetchone()[0]

def transfer_vendor(part_name, old_vendor, new_vendor):
    conn = psycopg2.connect(
        host="localhost", dbname="pp2_db",
        user="postgres", password="secret"
    )
    try:
        with conn:
            with conn.cursor() as cur:
                part_id     = get_or_create(cur, "parts",   "part_name",   part_name,   "part_id")
                old_vend_id = get_or_create(cur, "vendors", "vendor_name", old_vendor,  "vendor_id")
                new_vend_id = get_or_create(cur, "vendors", "vendor_name", new_vendor,  "vendor_id")

                cur.execute(
                    "DELETE FROM part_vendors WHERE part_id = %s AND vendor_id = %s;",
                    (part_id, old_vend_id)
                )
                cur.execute(
                    "INSERT INTO part_vendors (part_id, vendor_id) VALUES (%s, %s) ON CONFLICT DO NOTHING;",
                    (part_id, new_vend_id)
                )
        print(f"Vendor transferred: '{old_vendor}' → '{new_vendor}' for part '{part_name}'")
    except Exception as e:
        print(f"Transfer failed, rolled back: {e}")
    finally:
        conn.close()

transfer_vendor("Bolt M8", "Steel Corp", "Fasteners Ltd")
```

---

## 2. Call PostgreSQL Functions

A PostgreSQL **function** returns a value or a result set and is called with `SELECT`.
From Python you can call it with `callproc()` or `execute()`.

### Create the function in PostgreSQL

```sql
CREATE OR REPLACE FUNCTION get_parts_by_vendor(p_vendor_id INTEGER)
RETURNS TABLE (part_id INTEGER, part_name VARCHAR)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
        SELECT p.part_id, p.part_name
        FROM   parts p
        JOIN   part_vendors pv ON pv.part_id = p.part_id
        WHERE  pv.vendor_id = p_vendor_id;
END;
$$;
```

### Calling with `callproc()`

`callproc('function_name', (arg1, arg2, ...))` is equivalent to
`SELECT * FROM function_name(arg1, arg2);`

```python
import psycopg2

def get_parts_by_vendor(vendor_id):
    conn = psycopg2.connect(
        host="localhost", dbname="pp2_db",
        user="postgres", password="secret"
    )
    parts = []
    try:
        with conn.cursor() as cur:
            cur.callproc("get_parts_by_vendor", (vendor_id,))
            parts = cur.fetchall()      # list of (part_id, part_name) tuples
    finally:
        conn.close()
    return parts

rows = get_parts_by_vendor(1)
for part_id, part_name in rows:
    print(f"  {part_id}: {part_name}")
```

### Calling with `execute()` (alternative)

```python
import psycopg2

conn = psycopg2.connect(
    host="localhost", dbname="pp2_db",
    user="postgres", password="secret"
)

with conn.cursor() as cur:
    cur.execute("SELECT * FROM get_parts_by_vendor(%s);", (1,))
    for row in cur.fetchall():
        print(row)

conn.close()
```

### Calling a scalar function

```sql
CREATE OR REPLACE FUNCTION count_parts_for_vendor(p_vendor_id INTEGER)
RETURNS INTEGER
LANGUAGE sql
AS $$
    SELECT COUNT(*)::INTEGER
    FROM   part_vendors
    WHERE  vendor_id = p_vendor_id;
$$;
```

```python
import psycopg2

conn = psycopg2.connect(
    host="localhost", dbname="pp2_db",
    user="postgres", password="secret"
)

with conn.cursor() as cur:
    cur.callproc("count_parts_for_vendor", (1,))
    count = cur.fetchone()[0]
    print(f"Parts for vendor 1: {count}")

conn.close()
```

### Task 2

1. Create a PostgreSQL function `get_vendors_for_part(p_part_id INTEGER)` that returns
   `(vendor_id, vendor_name)` pairs for a given part.
2. Call it from Python using both `callproc()` and `execute()`.

**Solution:**

```sql
-- Run once in psql
CREATE OR REPLACE FUNCTION get_vendors_for_part(p_part_id INTEGER)
RETURNS TABLE (vendor_id INTEGER, vendor_name VARCHAR)
LANGUAGE sql
AS $$
    SELECT v.vendor_id, v.vendor_name
    FROM   vendors v
    JOIN   part_vendors pv ON pv.vendor_id = v.vendor_id
    WHERE  pv.part_id = p_part_id;
$$;
```

```python
import psycopg2

def get_vendors_for_part(part_id):
    conn = psycopg2.connect(
        host="localhost", dbname="pp2_db",
        user="postgres", password="secret"
    )
    try:
        with conn.cursor() as cur:
            # Using callproc
            cur.callproc("get_vendors_for_part", (part_id,))
            print("Via callproc:")
            for vid, vname in cur.fetchall():
                print(f"  {vid}: {vname}")

            # Using execute
            cur.execute("SELECT * FROM get_vendors_for_part(%s);", (part_id,))
            print("Via execute:")
            for vid, vname in cur.fetchall():
                print(f"  {vid}: {vname}")
    finally:
        conn.close()

get_vendors_for_part(1)
```

---

## 3. Call PostgreSQL Stored Procedures

A **stored procedure** performs an action (INSERT, UPDATE, DELETE) and is called with `CALL`.
Unlike functions, procedures do not return a result set — they modify data.

### Create the stored procedure in PostgreSQL

```sql
CREATE OR REPLACE PROCEDURE add_new_part(
    p_part_name   VARCHAR,
    p_vendor_name VARCHAR
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_part_id   INTEGER;
    v_vendor_id INTEGER;
BEGIN
    -- Insert part if it doesn't exist
    INSERT INTO parts (part_name)
    VALUES (p_part_name)
    ON CONFLICT DO NOTHING
    RETURNING part_id INTO v_part_id;

    IF v_part_id IS NULL THEN
        SELECT part_id INTO v_part_id FROM parts WHERE part_name = p_part_name;
    END IF;

    -- Insert vendor if it doesn't exist
    INSERT INTO vendors (vendor_name)
    VALUES (p_vendor_name)
    ON CONFLICT DO NOTHING
    RETURNING vendor_id INTO v_vendor_id;

    IF v_vendor_id IS NULL THEN
        SELECT vendor_id INTO v_vendor_id FROM vendors WHERE vendor_name = p_vendor_name;
    END IF;

    -- Link them
    INSERT INTO part_vendors (part_id, vendor_id)
    VALUES (v_part_id, v_vendor_id)
    ON CONFLICT DO NOTHING;
END;
$$;
```

### Calling the procedure from Python

```python
import psycopg2

def add_new_part(part_name, vendor_name):
    conn = psycopg2.connect(
        host="localhost", dbname="pp2_db",
        user="postgres", password="secret"
    )
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute("CALL add_new_part(%s, %s);", (part_name, vendor_name))
        print(f"Part '{part_name}' linked to vendor '{vendor_name}'.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()

add_new_part("Washer M8", "Steel Corp")
add_new_part("Bolt M10",  "Fasteners Ltd")
```

### Difference: function vs procedure

| | Function | Procedure |
|---|---|---|
| Called with | `SELECT` / `callproc()` | `CALL` / `execute('CALL ...')` |
| Returns | Value or table | Nothing (modifies data) |
| Transactions | Cannot commit/rollback inside | Can commit/rollback inside |
| Use case | Compute and return data | Perform actions |

### Task 3

1. Create a stored procedure `remove_vendor_from_part(p_part_name VARCHAR, p_vendor_name VARCHAR)`
   that removes the link between a part and a vendor.
2. Call it from Python.

**Solution:**

```sql
-- Run once in psql
CREATE OR REPLACE PROCEDURE remove_vendor_from_part(
    p_part_name   VARCHAR,
    p_vendor_name VARCHAR
)
LANGUAGE plpgsql
AS $$
BEGIN
    DELETE FROM part_vendors
    WHERE part_id  = (SELECT part_id   FROM parts   WHERE part_name   = p_part_name)
      AND vendor_id = (SELECT vendor_id FROM vendors WHERE vendor_name = p_vendor_name);
END;
$$;
```

```python
import psycopg2

def remove_vendor_from_part(part_name, vendor_name):
    conn = psycopg2.connect(
        host="localhost", dbname="pp2_db",
        user="postgres", password="secret"
    )
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute(
                    "CALL remove_vendor_from_part(%s, %s);",
                    (part_name, vendor_name)
                )
        print(f"Removed vendor '{vendor_name}' from part '{part_name}'.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()

remove_vendor_from_part("Bolt M8", "Steel Corp")
```

---

## 4. Work with BLOB Data (TODO at home)

PostgreSQL stores binary data with the `BYTEA` data type.
Use `psycopg2.Binary()` to wrap the data before inserting.

### Insert binary data (image / file)

```python
import psycopg2

def insert_drawing(part_id, file_path):
    with open(file_path, "rb") as f:
        data = f.read()

    file_ext = file_path.rsplit(".", 1)[-1]   # e.g. "png"

    conn = psycopg2.connect(
        host="localhost", dbname="pp2_db",
        user="postgres", password="secret"
    )
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO part_drawings (part_id, file_extension, drawing_data)
                    VALUES (%s, %s, %s);
                    """,
                    (part_id, file_ext, psycopg2.Binary(data))
                )
        print(f"Drawing inserted for part {part_id}.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()

insert_drawing(1, "bolt_m8.png")
```

### Select and save binary data

```python
import psycopg2
import os

def download_drawing(part_id, output_dir="./downloads"):
    conn = psycopg2.connect(
        host="localhost", dbname="pp2_db",
        user="postgres", password="secret"
    )
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT p.part_name, pd.file_extension, pd.drawing_data
                FROM   part_drawings pd
                JOIN   parts p ON p.part_id = pd.part_id
                WHERE  pd.part_id = %s;
                """,
                (part_id,)
            )
            row = cur.fetchone()
            if row is None:
                print(f"No drawing found for part {part_id}.")
                return

            part_name, file_ext, drawing_data = row
            os.makedirs(output_dir, exist_ok=True)
            file_path = os.path.join(output_dir, f"{part_name}.{file_ext}")

            with open(file_path, "wb") as f:
                f.write(drawing_data)

            print(f"Drawing saved to: {file_path}")
    finally:
        conn.close()

download_drawing(1)
```

### Insert and retrieve in one script

```python
import psycopg2
import os

DB_PARAMS = dict(
    host="localhost", dbname="pp2_db",
    user="postgres", password="secret"
)
SAMPLE_FILE = "sample.png"      # must exist in the working directory
OUTPUT_DIR  = "./downloads"

# --- INSERT ---
with open(SAMPLE_FILE, "rb") as f:
    binary_data = f.read()

ext = SAMPLE_FILE.rsplit(".", 1)[-1]

conn = psycopg2.connect(**DB_PARAMS)
with conn:
    with conn.cursor() as cur:
        # Make sure part_id=1 exists first
        cur.execute("SELECT part_id FROM parts WHERE part_id = 1;")
        if cur.fetchone():
            cur.execute(
                "INSERT INTO part_drawings (part_id, file_extension, drawing_data) VALUES (%s, %s, %s);",
                (1, ext, psycopg2.Binary(binary_data))
            )
            print("Binary data inserted.")
        else:
            print("Part with id=1 not found.")
conn.close()

# --- SELECT ---
conn = psycopg2.connect(**DB_PARAMS)
with conn.cursor() as cur:
    cur.execute(
        "SELECT p.part_name, pd.file_extension, pd.drawing_data "
        "FROM part_drawings pd JOIN parts p ON p.part_id = pd.part_id "
        "WHERE pd.part_id = 1 LIMIT 1;"
    )
    row = cur.fetchone()

if row:
    name, extension, data = row
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    out_path = os.path.join(OUTPUT_DIR, f"{name}.{extension}")
    with open(out_path, "wb") as f:
        f.write(data)
    print(f"File retrieved and saved: {out_path}")
conn.close()
```

### Task 4

Write two functions:
- `save_file(part_id, filepath)` — reads a file from disk and stores it in `part_drawings`.
- `load_file(part_id, output_dir)` — retrieves the file from the database and saves it to disk.

Test by saving and then loading any file (text, image, PDF).

**Solution:**

```python
import psycopg2
import os

DB_PARAMS = dict(
    host="localhost", dbname="pp2_db",
    user="postgres", password="secret"
)

def save_file(part_id, filepath):
    with open(filepath, "rb") as f:
        data = f.read()
    ext = filepath.rsplit(".", 1)[-1]

    conn = psycopg2.connect(**DB_PARAMS)
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO part_drawings (part_id, file_extension, drawing_data) "
                    "VALUES (%s, %s, %s);",
                    (part_id, ext, psycopg2.Binary(data))
                )
        print(f"Saved '{filepath}' for part_id={part_id}.")
    finally:
        conn.close()


def load_file(part_id, output_dir="./output"):
    conn = psycopg2.connect(**DB_PARAMS)
    try:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT p.part_name, pd.file_extension, pd.drawing_data "
                "FROM part_drawings pd "
                "JOIN parts p ON p.part_id = pd.part_id "
                "WHERE pd.part_id = %s LIMIT 1;",
                (part_id,)
            )
            row = cur.fetchone()

        if row is None:
            print(f"No file found for part_id={part_id}.")
            return

        part_name, ext, data = row
        os.makedirs(output_dir, exist_ok=True)
        out_path = os.path.join(output_dir, f"{part_name}.{ext}")
        with open(out_path, "wb") as f:
            f.write(data)
        print(f"Loaded file to '{out_path}'.")
    finally:
        conn.close()


# Test
save_file(1, "bolt_m8.png")
load_file(1, "./output")
```

---

## Conclusion

### Key Takeaways

**Transactions:**
- psycopg2 starts a transaction on the first SQL statement automatically
- `conn.commit()` — saves changes; `conn.rollback()` — discards changes
- Use `with conn:` context manager for automatic commit/rollback
- `conn.autocommit = True` for DDL and maintenance commands

**Calling Functions:**
- `cur.callproc('func_name', (args,))` — calls a PostgreSQL function
- Equivalent to `cur.execute("SELECT * FROM func_name(%s);", (args,))`
- `fetchone()` / `fetchall()` retrieves results as usual

**Calling Stored Procedures:**
- `cur.execute("CALL proc_name(%s, %s);", (arg1, arg2))` — executes a stored procedure
- Always `conn.commit()` after a procedure that modifies data
- Procedures modify data; functions return data — choose accordingly

**BLOB / Binary Data:**
- PostgreSQL uses `BYTEA`, not the SQL standard `BLOB` type
- Insert: wrap bytes with `psycopg2.Binary(data)` before passing to `execute()`
- Select: the returned value is already `bytes` — write directly with `open(..., 'wb')`
- Read files in binary mode: `open(path, 'rb').read()`
