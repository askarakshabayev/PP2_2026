import psycopg2

conn = psycopg2.connect(
    host="localhost",
    dbname="pp2_db",
    user="pp2",
    password="pp2_password"
)

cur = conn.cursor()

sql_select = "select id, name, email, grade from student order by grade limit 3;"

cur.execute(sql_select)
rows = cur.fetchall()

for row in rows:
    print(row)

cur.close()
conn.close()