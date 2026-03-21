import psycopg2

conn = psycopg2.connect(
    host="localhost",
    dbname="pp2_db",
    user="pp2",
    password="pp2_password"
)

cur = conn.cursor()

sql_delete = "delete from student where grade=100;"
cur.execute(sql_delete)
conn.commit()


cur.close()
conn.close()