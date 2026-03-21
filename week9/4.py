import psycopg2

conn = psycopg2.connect(
    host="localhost",
    dbname="pp2_db",
    user="pp2",
    password="pp2_password"
)

cur = conn.cursor()

sql_courses = """
    create table if not exists courses (
        id serial primary key,
        title varchar(200) not null,
        code varchar(20) unique not null
    )
"""

cur.execute(sql_courses)

sql_enrollments = """
    create table if not exists enrollments (
        id serial primary key,
        student_id integer references student(id) on delete cascade,
        course_id integer references courses(id) on delete cascade,
        score float
    )
"""

cur.execute(sql_enrollments)
conn.commit()

print("Tables created!!!")
cur.close()
conn.close()