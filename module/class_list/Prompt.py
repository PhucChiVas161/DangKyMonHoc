from module.class_list.CourseManager import CourseManager
from colorama import Fore, Style
from tabulate import tabulate

class Prompt:
    def askTheoryClassId(typeId):
        while True:
            classOrder = input("Nhập STT môn cần đăng ký: ")
            try:
                courseFound = CourseManager.getCourse(int(classOrder))
            except:
                print("Vui lòng nhập đúng STT môn học cần đăng ký! ")
                continue
            if(courseFound is None):
                print("Không tìm thấy môn học.")
                continue
            else:
                return f"https://regist.vlu.edu.vn/DangKyHocPhan/DangKy?Hide={courseFound.id}|&acceptConflict=false&classStudyUnitConflictId=&RegistType={typeId}&ScheduleStudyUnitID="
    def askTheoryAndPracticeClassId(typeId):
        while True:
            try:
                theoryClassOrder = input("Nhập STT lớp LÝ THUYẾT cần đăng ký: ")
                if(theoryClassOrder=="x"):
                    break
                theoryCourseFound = CourseManager.getCourse(int(theoryClassOrder))
                if(theoryCourseFound is None):
                    print("Không tìm thấy môn học.")
                    continue

                practiceCourses = CourseManager.getCoursesByTheoryCode(theoryCourseFound.code)

                practiceClassData = [practiceCourse.getArrayData() for practiceCourse in practiceCourses]

                print(f"Có {len(practiceCourses)} lớp thực thành tương ứng với {theoryCourseFound.code}:\n")
                print(Fore.BLUE + Style.NORMAL + (tabulate(practiceClassData, headers=theoryCourseFound.headers, tablefmt='mixed_grid')))

                practiceClassOrder = input("\nNhập STT lớp THỰC HÀNH cần đăng ký: ")

                practiceCourseFound = CourseManager.getCourse(int(practiceClassOrder))
                if(practiceCourseFound is None):
                    print("Không tìm thấy môn học.")
                    continue
                return f"https://regist.vlu.edu.vn/DangKyHocPhan/DangKy?Hide={theoryCourseFound.id}|{
        practiceCourseFound.id}|&acceptConflict=false&classStudyUnitConflictId=&RegistType={typeId}&ScheduleStudyUnitID="
            except:
                print("Nhập 'x' để thoát.")
                continue
            
