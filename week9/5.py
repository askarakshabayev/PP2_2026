import psycopg2

conn = psycopg2.connect(
    host="localhost",
    dbname="pp2_db",
    user="pp2",
    password="pp2_password"
)

cur = conn.cursor()

sql_books = """
    create table if not exists books (
        id serial primary key,
        title varchar(100) not null,
        author varchar(100) not null,
        price float,
        in_stock boolean default true
    )
"""

cur.execute(sql_books)
conn.commit()
print("Table created")

cur.close()
conn.close()