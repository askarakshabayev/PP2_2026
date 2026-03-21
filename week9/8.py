import psycopg2

conn = psycopg2.connect(
    host="localhost",
    dbname="pp2_db",
    user="pp2",
    password="pp2_password"
)

cur = conn.cursor()

sql_update = """
    update student set grade=%s where grade>=%s;
"""

cur.execute(
    sql_update,
    (100, 97)
)
conn.commit()
cur.close()
conn.close()