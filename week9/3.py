import psycopg2

conn = psycopg2.connect(
    host="localhost",
    dbname="pp2_db",
    user="pp2",
    password="pp2_password"
)

cur = conn.cursor()

sql_text = """
    create table if not exists student (
        id SERIAL primary key,
        name varchar(100) not null,
        email varchar(100) unique not null,
        grade float,
        enrolled boolean default TRUE,
        created_at timestamp default current_timestamp
    );
"""

cur.execute(sql_text)
conn.commit()
print("Table created")

cur.close()
conn.close()