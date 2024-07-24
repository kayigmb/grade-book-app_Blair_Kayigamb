import sqlite3


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
            print(f"\n{e}\n")
