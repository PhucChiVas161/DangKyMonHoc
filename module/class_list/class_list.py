from bs4 import BeautifulSoup
from module.class_list.Prompt import Prompt
from module.class_list.CourseManager import CourseManager
from module.class_list.Handler import Handler
from module.random_fact import random_fact
from colorama import Fore
import time


def viewTheoryAndPracticeClass(session, course_id, typeId):
    while True:
        response = session.get(
            f"https://regist.vlu.edu.vn/DangKyHocPhan/DanhSachLopHocPhan?id={course_id}&registType={typeId}&scheduleStudyUnitID="
        )
        if response.status_code != 200:
            print(Fore.RED + f"Server lỗi, đang thử lại...-{random_fact()}")
            time.sleep(3)
        else:
            break
    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find("table")
    tbody = table.find("tbody")
    trCount = tbody.find_all(recursive=False)
    excludeName = "thực hành"
    stt = 1
    for i in range(0, len(trCount)):
        row = trCount[i]
        if i % 2 == 0:
            theoryCourse = Handler.viewTheoryClass(row, stt)
            CourseManager.courses.append(theoryCourse)
        else:
            span = row.find("span")
            if span != None:
                if excludeName in span.get_text():
                    CourseManager.isForTheoryClass = False
                    practiceCourses = Handler.viewPracticeClass(stt, row, theoryCourse)
                    stt += len(practiceCourses) - 1
                    CourseManager.courses.extend(practiceCourses)
            else:
                theoryCourse = Handler.viewTheoryClass(row, stt)
                CourseManager.courses.append(theoryCourse)
        stt += 1


def decidePrompt(typeId):
    if CourseManager.isForTheoryClass:
        return Prompt.askTheoryClassId(typeId)
    else:
        return Prompt.askTheoryAndPracticeClassId(typeId)
