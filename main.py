# usr/bin/python3
# Alu project grade book app
import sqlite3

from courses import course
from gradebook import gradebook
from students import student

connection = sqlite3.connect("gradebook.db")
cursor = connection.cursor()

cursor.execute(
    """
        CREATE TABLE IF NOT EXISTS students (
            name TEXT,
            email TEXT,
            gpa INTEGER DEFAULT 0.0
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

cursor.execute(
    """
        CREATE TABLE IF NOT EXISTS gradebook(
            email TEXT,
            course TEXT,
            grade INTEGER DEFAULT 0
        ) 
        
    """
)


def create_student() -> None:
    name = input("Enter student name: ")
    email = input("Enter student email: ")
    student(name=name, email=email).add_student()
    print(f"\n\aStudent {name} has been successfully registered")


def create_course():
    while True:
        try:
            name = input("Enter course name: ")
            trimester = input("Enter course trimester: ")
            credits = int(input("Enter course credits: "))
            course(name=name, trimester=trimester, credits=credits).add_course()
        except ValueError:
            print("\nCredits should be a number")
        else:
            print(f"\nCourse {name} has been successfully registered")
            break


def search_student_by_grade():
    while True:
        try:
            min_gpa = int(input("Enter minimum gpa: "))
            max_gpa = int(input("Enter maximum gpa: "))
        except ValueError:
            print("\nIncorrect input of minimum or maximum gpa\n")
        else:
            student().load_all_student_with_gpa(min_gpa=min_gpa, max_gpa=max_gpa)
            break


def register_student_to_course():
    while True:
        try:
            email = input("Enter student email: ")
            student_email = cursor.execute(
                """
                   SELECT * FROM students WHERE email = ?
                """,
                (email,),
            )
            if not student_email.fetchone():
                raise ValueError("Student is not found")
            c_name = input("Enter course: ")
            course_name = cursor.execute(
                """
                    SELECT * FROM courses  WHERE name=?
                """,
                (c_name,),
            )
            if not course_name.fetchone():
                raise ValueError("Course is not found")
            gradebook(email=email, course=c_name).register_student_grade()
        except Exception as e:
            print(f"\n{e}\n")
        else:
            print(f"\nStudent {email} has been registerred to {c_name} course")
            break


def update_student_grades():
    while True:
        try:
            email = input("Enter student email: ")
            student_email = cursor.execute(
                """
                   SELECT * FROM gradebook WHERE email = ?
                """,
                (email,),
            )
            if not student_email.fetchone():
                raise ValueError("Student is not found")
            course = input("Enter course: ")
            course_name = cursor.execute(
                """
                   SELECT * FROM gradebook WHERE course = ?
                """,
                (course,),
            )
            if not course_name.fetchone():
                raise ValueError(f"{email} is not registered to this course")
            grade = int(input("Enter student grade: "))
            gradebook(email=email, course=course, grade=grade).update_student_grade()
        except Exception as e:
            print(f"\n{e}\n")
        else:
            print(f"\nStudent {email} grades have been upgraded successfully")
            calculate_gpa(email)
            break


def calculate_gpa(email):
    try:
        student_data = cursor.execute(
            """
                   SELECT * FROM gradebook WHERE email = ?
                """,
            (email,),
        )
        total_grade = 0
        courses = 0
        for grade in student_data.fetchall():
            total_grade = total_grade + grade[2]
            courses += 1
        avg_grade_from_all_courses = total_grade / courses
        calc_gpa = round((avg_grade_from_all_courses / 100 * 4), 2)
        student(gpa=calc_gpa, email=email).update_student_grades()
    except Exception as e:
        raise e


def menu():
    print("\n----------------------------------")
    print("WELCOME TO THE GRADE BOOK APP")
    print("----------------------------------")
    print("\n1. Create a student")
    print("2. create a course")
    print("3. Register a student to a course")
    print("4. Update Student grades")
    print("5. Generate students transcripts")
    print("6. Search student by gpa")
    print("7. Exit\n")


def gradebook_app():
    while True:
        menu()
        try:
            value = int(input("Choose a service: "))
        except Exception:
            print("\nWrong Input")
            continue

        print()
        match value:
            case 1:
                create_student()
            case 2:
                create_course()
            case 3:
                register_student_to_course()
            case 4:
                update_student_grades()
            case 5:
                student().load_transcipts_for_all_students()
            case 6:
                search_student_by_grade()
            case 7:
                print("\nBye! Thank you for using the platform")
                break
            case _:
                print("\nInvalid Service")


if __name__ == "__main__":
    gradebook_app()

connection.commit()
connection.close()
