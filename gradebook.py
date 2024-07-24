import sqlite3


class gradebook:
    def __init__(self, email="", course="", grade=-1):
        self.email = email
        self.course = course
        self.grade = grade
        self.connection = sqlite3.connect("gradebook.db")
        self.cursor = self.connection.cursor()

    def register_student_grade(self):
        self.cursor.execute(
            """
                INSERT INTO gradebook(email,course,grade) 
                VALUES (?,?,?) 
            """,
            (self.email, self.course, self.grade),
        )
        self.connection.commit()

    def update_student_grade(self):
        self.cursor.execute(
            """
                UPDATE gradebook
                SET grade = ?
                WHERE email = ? AND course = ?
            """,
            (self.grade, self.email, self.course),
        )
        self.connection.commit()
