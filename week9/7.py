import psycopg2

conn = psycopg2.connect(
    host="localhost",
    dbname="pp2_db",
    user="pp2",
    password="pp2_password"
)

cur = conn.cursor()

sql_ins = """
    insert into student(name, email, grade) values(%s, %s, %s) returning id;
"""

students = [
    ("Name1", "email1@gmail.com", 87),
    ("Name2", "email2@gmail.com", 90),
    ("Name3", "email3@gmail.com", 56)
]

cur.executemany(
    sql_ins,
    students
)

conn.commit()
print(cur.rowcount)

cur.close()
conn.close()