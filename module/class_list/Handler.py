from tabulate import tabulate
from colorama import Fore, Style
from typing import List
from module.class_list.Course import Course


class Handler:
    def theoryClassDecorator(func):
        def wrapper(*args, **kwargs):
            print(Style.BRIGHT + Fore.GREEN + "\n Bảng lý thuyết:")
            result = func(*args, **kwargs)
            return result

        return wrapper

    @staticmethod
    @theoryClassDecorator
    def viewTheoryClass(row, stt) -> Course:
        cells = row.find_all("td")
        row_data = [
            cell.get_text(strip=True) for cell in cells if not cell.find("span")
        ]
        courseId = row.find("input").get("id")
        course = Course(
            stt,
            type=row_data[1],
            code=row_data[2],
            remain=row_data[4],
            schedule=row_data[5],
            note=row_data[7],
            id=courseId,
        )

        print(
            Fore.GREEN
            + Style.NORMAL
            + (
                tabulate(
                    [course.getArrayData()],
                    headers=course.headers,
                    tablefmt="fancy_grid",
                )
            )
        )
        return course

    def practiceClassDecorator(func):
        def wrapper(*args, **kwargs):
            print("-" * 100)
            print(
                Fore.CYAN + Style.BRIGHT + """│\n└── Bảng thực hành tương ứng với:""",
                args[2].code,
            )
            result = func(*args, **kwargs)
            print("*" * 120)
            return result

        return wrapper

    @staticmethod
    @practiceClassDecorator
    def viewPracticeClass(stt, row, theoryCourse: Course) -> List[Course]:
        courses: List[Course] = []
        rowsOfClass = row.find_all("tr")
        for t in rowsOfClass[1:]:  # exclude header
            tds = t.find_all("td")
            course = Course(
                order=stt,
                type="Thực hành",
                code=tds[1].getText(strip=True),
                remain=tds[2].getText(strip=True),
                schedule=tds[3].getText(strip=True),
                note=tds[4].getText(strip=True),
                id=tds[0].find("input").get("id"),
            )
            stt += 1
            courses.append(course)
            print(
                Fore.BLUE
                + Style.NORMAL
                + (
                    tabulate(
                        [course.getArrayData()],
                        headers=course.headers,
                        tablefmt="mixed_grid",
                    )
                )
            )
        return courses
