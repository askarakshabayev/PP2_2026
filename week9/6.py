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
# cur.execute(sql_ins, ("Abzal", "Kairatov", 95))
# cur.execute(sql_ins, ("QQQ", "Bbbb", 67))
cur.execute(sql_ins, ("A3", "B3", 98))
new_id = cur.fetchone()[0]
print(new_id)
conn.commit()

print("Row inserted")

cur.close()
conn.close()