import psycopg2

conn = psycopg2.connect(
    host="localhost",
    port=5432,
    dbname="pp2_db",
    user="pp2",
    password="pp2_password"
)

cur = conn.cursor()
print("Connected:", conn.status)

cur.close()
conn.close()