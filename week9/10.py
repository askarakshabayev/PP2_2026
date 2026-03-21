import psycopg2

conn = psycopg2.connect(
    host="localhost",
    dbname="pp2_db",
    user="pp2",
    password="pp2_password"
)

cur = conn.cursor()

cur.execute("SELECT COUNT(*), AVG(grade), MAX(grade), MIN(grade) FROM student;")
count, avg, mx, mn = cur.fetchone()
print(f"Count={count}  Avg={avg:.1f}  Max={mx}  Min={mn}")

cur.close()
conn.close()