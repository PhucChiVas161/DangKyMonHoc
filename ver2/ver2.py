from bs4 import BeautifulSoup
from Prompt import Prompt
from CourseManager import CourseManager
from Handler import Handler
import sys, os

source_path = sys._MEIPASS if hasattr(sys, "_MEIPASS") else os.path.abspath("./draft")
file_path = os.path.join(source_path, "DanhSachLopHocPhan.txt")
f = open(file_path, encoding="utf-8")
# f = open("../draft/DanhSachLopHocPhan.txt", encoding="utf-8")
data = f.read()
soup = BeautifulSoup(data, "html.parser")
table = soup.find("table")
tbody = table.find("tbody")
trCount = tbody.find_all(recursive=False)


def viewTheoryAndPracticeClass():
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


def decidePrompt():
    if CourseManager.isForTheoryClass:
        Prompt.askTheoryClassId()
    else:
        Prompt.askTheoryAndPracticeClassId()


if __name__ == "__main__":
    viewTheoryAndPracticeClass()
    decidePrompt()
