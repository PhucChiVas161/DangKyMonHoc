from bs4 import BeautifulSoup
from tabulate import tabulate
from colorama import Fore, Style
from pprint import pprint
from typing import List

class Course:
    headers = ['STT', 'Loại', 'Mã LHP', 'Số lượng', 'Lịch học', 'Ghi chú', 'ID lớp lý thuyết']
    def __init__(self, order: int = -1, type: str = "", code: str = "", remain: str = "", schedule: str = "", note: str = "", id: str = ""):
        self.order = order
        self.type = type
        self.code = code
        self.remain = remain
        self.schedule = schedule
        self.note = note
        self.id = id

    def getArrayData(self) -> List:
        return [
            self.order,
            self.type,
            self.code,
            self.remain,
            self.schedule,
            self.note,
            self.id,
        ]
    
    def getCode(self):
        return self.code

class CourseManager:
    courses : List[Course]= []

    @staticmethod
    def getCourse(order: int) -> Course | None:
        for course in CourseManager.courses:
            if(course.order == order):
                return course
        return None

f = open("./draft/DanhSachLopCo1Loai.txt", encoding="utf-8")
data = f.read()
soup = BeautifulSoup(data, 'html.parser')
table = soup.find('table')
tbody = table.find('tbody')
trCount = tbody.find_all(recursive=False)


def theoryClassDecorator(func):
    def wrapper(*args, **kwargs):
        print(Style.BRIGHT + Fore.GREEN + '\n Bảng lý thuyết:')
        result = func(*args, **kwargs)
        return result
    return wrapper

@theoryClassDecorator
def viewTheoryClass(row, stt) -> Course:
    cells = row.find_all('td')
    row_data = [cell.get_text(strip=True) for cell in cells if not cell.find('span')]
    # pprint(row_data)
    courseId = row.find('input').get('id')
    course = Course(stt, type=row_data[1],code=row_data[2], remain=row_data[4], schedule=row_data[5], note=row_data[7], id=courseId)
    
    print(Fore.GREEN + Style.NORMAL + (tabulate([course.getArrayData()], headers=course.headers, tablefmt='fancy_grid')))
    return course


def practiceClassDecorator(func):
    def wrapper(*args, **kwargs):
        print(Fore.BLUE + Style.BRIGHT + '''│\n└── Bảng thực hành tương ứng với:''', args[2].getCode())
        result = func(*args, **kwargs)
        print("-/"*90)
        return result
    return wrapper

@practiceClassDecorator
def viewPracticeClass(stt, row, theoryCourse: Course) -> List[Course]:
    courses : List[Course] = []
    rowsOfClass = row.find_all('tr')
    for t in rowsOfClass[1:]: # exclude header
        tds = t.find_all('td')
        course = Course(
            order=stt,
            type="Thực hành",
            code=tds[1].getText(strip=True),
            remain=tds[2].getText(strip=True),
            schedule=tds[3].getText(strip=True),
            note=tds[4].getText(strip=True),
            id=tds[0].find('input').get('id')
        )
        stt+=1
        courses.append(course)
        print(Fore.BLUE + Style.NORMAL + (tabulate([course.getArrayData()], headers=course.headers, tablefmt='mixed_grid')))
    return courses

def viewTheoryAndPracticeClass():
    excludeName = "thực hành"
    stt = 1
    for i in range(0, len(trCount)):
        row = trCount[i]
        if (i % 2 == 0):
            theoryCourse = viewTheoryClass(row, stt)
            CourseManager.courses.append(theoryCourse)
        else:
            span = row.find('span')
            if(span!=None):
                if(excludeName in span.get_text()):
                    practiceCourses = viewPracticeClass(stt, row, theoryCourse)
                    stt += len(practiceCourses) -1
                    CourseManager.courses.extend(practiceCourses)
            else:
                theoryCourse = viewTheoryClass(row, stt)
                CourseManager.courses.append(theoryCourse)
        stt+=1

def prompt(hint: str):
    while True:
        return input(hint)

def askCourseCode():
    while True:
        classOrder = prompt("Please choose class by order number: ")
        try:
            courseFound = CourseManager.getCourse(int(classOrder))
        except:
            print("Please type correct course order!")
            continue
        if(courseFound is None):
            print("Course not found.")
            continue
        else:
            print("Your course code id: ",courseFound.code)
            break

if __name__ == "__main__":
    viewTheoryAndPracticeClass()
    askCourseCode()
    
   