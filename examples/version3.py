from version1 import choose_course
from PyMemAPI import Course
from getpass import getpass


if __name__ == "__main__":
    # Enter username and password here
    __username__ = input("Enter username: ")
    __password__ = getpass("Enter password: ")

    course: Course = choose_course(__username__, __password__)
    custom = {
        "1": "14092053",
        "5": "14092052",
    }
    status = course.move_level(8, 5, custom)
    if status:
        print("Success")
