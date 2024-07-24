# Alu project grade book app
import sqlite3

connection = sqlite3.connect("gradebook.db")
cursor = connection.cursor()

cursor.execute(
    """
        CREATE TABLE IF NOT EXISTS students (
            name TEXT,
            course TEXT,
            email TEXT,
            gpa INTEGER DEFAULT 0
            ) 
    """
)

cursor.execute(
    """
        CREATE TABLE IF NOT EXISTS courses(
            name TEXT,
            trimester TEXT,
            credits INTEGER
        ) 
        
    """
)


class student:

    def __init__(self, name="", email="", course="", gpa=-1):
        self.email = email
        self.name = name
        self.course = course
        self.gpa = gpa
        self.connection = sqlite3.connect("gradebook.db")
        self.cursor = self.connection.cursor()

    def add_student(self):
        self.cursor.execute(
            """
                INSERT INTO students(name,email) 
                VALUES (?,?) 
            """,
            (self.name, self.email),
        )
        self.connection.commit()

    def enroll_student_to_course(self, course):
        self.cursor.execute(
            """
                UPDATE students
                SET course = ?
                WHERE email = ?
            """,
            (course, self.email),
        )
        self.connection.commit()
        print("Student {self.email} has been successfully register to {course} course")

    def load_student_by_email(self, email):
        try:
            self.cursor.execute(
                """
                    SELECT * FROM students WHERE email = (?) 
                """,
                (email,),
            )
            data = self.cursor.fetchall()
            if not data:
                raise ValueError("USER NOT FOUND")
            print(data)
        except ValueError as e:
            print(e)

    def load_all_student(self):
        try:
            self.cursor.execute(
                """
                    SELECT * FROM students 
                """
            )
            data = self.cursor.fetchall()
            if not data:
                raise ValueError("USER NOT FOUND")

            print("Name\tEmail\tCourse\tGPA")
            print("---------------------------------------------")
            for records in data:
                print(f"{records[0]}\t{records[1]}\t{records[2]}\t{records[3]}")
        except ValueError as e:
            print(e)

    def load_all_student_with_gpa(self, min_gpa):
        try:
            self.cursor.execute(
                """
                    SELECT * FROM students WHERE gpa >= ? 
                """,
                (min_gpa,),
            )
            data = self.cursor.fetchall()
            if not data:
                raise ValueError("USERS NOT FOUND")
            print("Name\tGPA")
            print("---------------------------------------------")
            for records in data:
                print(f"{records[0]}\t{records[3]}")

        except ValueError as e:
            print(e)


class course:

    def __init__(self, name="", trimester="", credits=-1):
        self.trimester = trimester
        self.name = name
        self.credits = credits
        self.connection = sqlite3.connect("gradebook.db")
        self.cursor = self.connection.cursor()

    def add_course(self):
        self.cursor.execute(
            """
                INSERT INTO courses(name,trimester,credits) 
                VALUES (?,?,?) 
            """,
            (self.name, self.trimester, self.credits),
        )
        self.connection.commit()

    def load_all_courses(self):
        try:
            self.cursor.execute(
                """
                    SELECT * FROM courses 
                """
            )
            data = self.cursor.fetchall()
            if not data:
                raise ValueError("COURSES NOT FOUND")
            print("CourseName\tTrimester\tCredits")
            print("---------------------------------------------")
            for records in data:
                print(f"{records[0]}\t{records[1].strip()}\t{records[2]}")
        except ValueError as e:
            print(e)


def create_student():
    name = input("Enter student name: ")
    email = input("Enter student email: ")
    student(name=name, email=email).add_student()
    print(f"Student {name} has been successfully registered")


def create_course():
    while True:
        try:
            name = input("Enter course name: ")
            trimester = input("Enter course trimester: ")
            credits = int(input("Enter course course: "))
            course(name=name, trimester=trimester, credits=credits).add_course()
        except ValueError:
            print("Credits should be a number")
        else:
            print(f"Course {name} has been successfully registered")
            break


def register_student_to_course():
    while True:
        try:
            email = input("Enter Student email: ")
            course = input("Enter course name: ")
            student_record = cursor.execute(
                """
                    SELECT * FROM students  WHERE email = ?
                """,
                (email,),
            )
            if student_record.fetchone() is None:
                raise ValueError(f"Student {email} is unavailable")
            course_record = cursor.execute(
                """
                    SELECT * FROM courses  WHERE name = ?
                """,
                (course,),
            )
            if course_record.fetchone() is None:
                raise ValueError(f"Course {course} is unavailable")
            student(email=email).enroll_student_to_course(course)
            break
        except ValueError as e:
            print(e)


# course().load_all_courses()
# student().load_all_student()
# register_student_to_course()
# course().load_all_courses()
# create_course()
# course().add_all_courses()
# create_student()
student().load_all_student()
# student().load_student_by_email("fa")
# student().load_all_student_with_gpa(0)
connection.commit()
connection.close()
