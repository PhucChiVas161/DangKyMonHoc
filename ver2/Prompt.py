from CourseManager import CourseManager
from colorama import Fore, Style
from tabulate import tabulate

class Prompt:
    def askTheoryClassId():
        while True:
            classOrder = input("Please choose class by order number: ")
            try:
                courseFound = CourseManager.getCourse(int(classOrder))
            except:
                print("Please type correct course order!")
                continue
            if(courseFound is None):
                print("Course not found.")
                continue
            else:
                print("Your course code id: ",courseFound.id)
                break
    def askTheoryAndPracticeClassId():
        while True:
            try:
                theoryClassOrder = input("Please choose theory class by order number: ")
                if(theoryClassOrder=="x"):
                    break
                theoryCourseFound = CourseManager.getCourse(int(theoryClassOrder))
                if(theoryCourseFound is None):
                    print("Course not found.")
                    continue

                print("Your course code id: ",theoryCourseFound.id)
                practiceCourses = CourseManager.getCoursesByTheoryCode(theoryCourseFound.code)

                practiceClassData = [practiceCourse.getArrayData() for practiceCourse in practiceCourses]

                print(f"There are {len(practiceCourses)} practice classes of {theoryCourseFound.code}:\n")
                print(Fore.BLUE + Style.NORMAL + (tabulate(practiceClassData, headers=theoryCourseFound.headers, tablefmt='mixed_grid')))

                practiceClassOrder = input("\nPlease choose practice class above by order number: ")

                practiceCourseFound = CourseManager.getCourse(int(practiceClassOrder))
                if(practiceCourseFound is None):
                    print("Course not found.")
                    continue

                print(f"Your course code id: {theoryCourseFound.id}|{practiceCourseFound.id}")
                break
            except:
                print("Please type correct course order or enter x to escape.")
                continue
            