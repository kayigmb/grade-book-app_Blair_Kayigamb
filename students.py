import sqlite3


class student:

    def __init__(self, name="", email="", gpa=-1.0):
        self.email = email
        self.name = name
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

    def load_all_student_with_gpa(self, min_gpa, max_gpa):
        try:
            self.cursor.execute(
                """
                    SELECT * FROM students WHERE gpa >= ? AND gpa <= ? ORDER BY gpa DESC 
                """,
                (min_gpa, max_gpa),
            )
            data = self.cursor.fetchall()
            if not data:
                raise ValueError("\nUSERS NOT FOUND")
            print("\nName\tGPA")
            print("---------------------------------------------")
            for records in data:
                print(f"\n{records[0]}\t{records[2]}\n")
        except ValueError as e:
            print(f"\n{e}\n")

    def load_transcipts_for_all_students(self):
        try:
            data = self.cursor.execute(
                """
                    SELECT * FROM students ORDER BY gpa DESC 
                """
            )
            data = self.cursor.fetchall()
            if not data:
                raise ValueError("\nUSERS NOT FOUND")
            print("\nstudent transcipt")
            print("-------------------------")
            for record in data:
                print(f"\nName of the student: {record[0].capitalize()}{record[1]}")
                print(f"GPA: {record[2]}\n")
        except Exception as e:
            print(f"\n{e}\n")

    def update_student_grades(self):
        self.cursor.execute(
            """
                    UPDATE students
                    SET gpa = ?
                    WHERE email = ?
                """,
            (self.gpa, self.email),
        )
        self.connection.commit()
