import psycopg2
import csv

# with open('user.csv', 'r') as f:
#     reader = csv.DictReader(f)
#     conn = psycopg2.connect(
#         host='localhost',
#         database='phonebook_db',
#         user='phonebook_db',
#         password='phonebook_db'

#     )
#     cur = conn.cursor()
#     for row in reader:
#         print(row)
#         cur.execute("insert into phonebook (fio, phone) values (%s, %s)", (row['fio'], row['phone']))

#     conn.commit()

# cur.close()
# conn.close()


# conn = psycopg2.connect(
#     host='localhost',
#     database='phonebook_db',
#     user='phonebook_db',
#     password='phonebook_db'
# )

# cur = conn.cursor()
# cur.execute("select * from phonebook")
# rows = cur.fetchall()

# for row in rows:
#     print(row)

# conn = psycopg2.connect(
#     host='localhost',
#     database='phonebook_db',
#     user='phonebook_db',
#     password='phonebook_db'
# )
# cur = conn.cursor()

# sql_text = """
#     create table books(
#         id serial primary key,
#         title varchar(100),
#         author varchar(100),
#         price float,
#         in_stock boolean default true    
#     );
# """
# cur.execute(sql_text)
# conn.commit()
# conn = psycopg2.connect(
#     host='localhost',
#     database='phonebook_db',
#     user='phonebook_db',
#     password='phonebook_db'
# )
# cur = conn.cursor()

# books = (
#     ("Clean Code", "Robert Martin", 35.99),
#     ("The Pragmatic Programmer", "David Thomas", 42.00),
#     ("Python Crash Course", "Eric Matthes", 29.99)
# )

# cur.executemany("insert into books (title, author, price) values(%s, %s, %s);", books)
# conn.commit()

conn = psycopg2.connect(
    host='localhost',
    database='phonebook_db',
    user='phonebook_db',
    password='phonebook_db'
)
cur = conn.cursor()

# try:
#     cur.execute("insert into parts(part_name) values %s returning part_id", ("Bolt M8",))
#     part_id = cur.fetchone()[0]
    
#     cur.execute(
#         "INSERT INTO vendors (vendor_name) VALUES (%s) RETURNING vendor_id;",
#         ("Steel Corp",)
#     )
#     vendor_id = cur.fetchone()[0]

#     # Link part to vendor
#     cur.execute(
#         "INSERT INTO part_vendors (part_id, vendor_id) VALUES (%s, %s);",
#         (part_id, vendor_id)
#     )

#     conn.commit()
#     print(f"Transaction committed. part_id={part_id}, vendor_id={vendor_id}")

# except:
#     pass

def get_parts_by_vendors(vendor_id):
    cur.callproc("get_parts_by_vendor", (vendor_id, ))
    parts = cur.fetchall()
    return parts

rows = get_parts_by_vendors(1)
print(rows)

cur.close()
conn.close()