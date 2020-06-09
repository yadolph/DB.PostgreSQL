import psycopg2 as pg

def create_db():
    with pg.connect(database='netology', user='netology', password='netology', host='localhost', port=5432) as conn:
        cur = conn.cursor()

        cur.execute('DROP TABLE student_course;')
        cur.execute('DROP TABLE student;')
        cur.execute('DROP TABLE course;')

        cur.execute('''CREATE TABLE IF NOT EXISTS student (
                id SERIAL PRIMARY KEY NOT NULL,
                name VARCHAR(100) NOT NULL,
                gpa NUMERIC(10, 2),
                birth TIMESTAMPTZ
            );''')

        cur.execute('''CREATE TABLE IF NOT EXISTS course (
                 id SERIAL PRIMARY KEY NOT NULL,
                 name VARCHAR(100) NOT NULL
             );''')

        cur.execute('''CREATE TABLE IF NOT EXISTS student_course (
            student_id INT REFERENCES student(id),
            course_id INT REFERENCES course(id),
            CONSTRAINT student_course_pk PRIMARY KEY(student_id, course_id)
        );''')

        cur.execute('INSERT INTO course(name) VALUES (%s);',('python',))
        cur.execute('INSERT INTO course(name) VALUES (%s);',('javascript',))


def add_students(course_id, students):
    if len(students) == 1:
        with pg.connect(database='netology', user='netology', password='netology', host='localhost', port=5432) as conn:
            cur = conn.cursor()
            cur.execute('INSERT INTO student(name, gpa, birth) VALUES (%s, %s, %s) RETURNING id;',
                        (students['name'], students['gpa'], students['birth']))

            student_id = cur.fetchone()

            cur.execute('INSERT INTO student_course(course_id, student_id) VALUES (%s, %s);', (course_id, student_id,))

            conn.commit()

    elif len(students) > 1:
        for student in students:
            with pg.connect(database='netology', user='netology', password='netology', host='localhost', port=5432) as conn:
                cur = conn.cursor()
                cur.execute('INSERT INTO student(name, gpa, birth) VALUES (%s, %s, %s) RETURNING id;',
                            (student['name'], student['gpa'], student['birth']))

                student_id = cur.fetchone()

                cur.execute('INSERT INTO student_course(course_id, student_id) VALUES (%s, %s);', (course_id, student_id,))

                conn.commit()


def add_student(student):
    with pg.connect(database='netology', user='netology', password='netology', host='localhost', port=5432) as conn:
        cur = conn.cursor()
        cur.execute('INSERT INTO student(name, gpa, birth) VALUES (%s, %s, %s);',
                    (student['name'], student['gpa'], student['birth']))
        conn.commit()

def get_student(student_id):
    with pg.connect(database='netology', user='netology', password='netology', host='localhost', port=5432) as conn:
        cur = conn.cursor()
        cur.execute('SELECT * FROM student WHERE id = %s;', (student_id,))
        student = cur.fetchall()
        return student

def get_students(course_id):
    with pg.connect(database='netology', user='netology', password='netology', host='localhost', port=5432) as conn:
        cur = conn.cursor()
        cur.execute('SELECT * FROM student_course WHERE course_id = %s;', (course_id,))
        student_ids = cur.fetchall()
        student_list = []
        for student_id in student_ids:
            cur.execute('SELECT * FROM student WHERE id = %s;', (student_id[0],))
            student = cur.fetchall()
            student_list.append(student)
        return student_list


if __name__ == '__main__':

    students = [{'name': 'Vova', 'gpa': 4.2, 'birth': '1998-06-22 00:00:00+05'},
                {'name': 'Sega', 'gpa': 3.8, 'birth': '1997-03-17 00:00:00+05'}]

    student = {'name': 'Masha', 'gpa': 4.5, 'birth': '1999-02-23 00:00:00+05'}

    create_db()
    add_students(1, students)
    add_student(student)
    print(get_student(2))
    print(get_students(1))