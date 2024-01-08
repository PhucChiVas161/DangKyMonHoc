from typing import List
from Course import Course

class CourseManager:
    isForTheoryClass = True
    courses : List[Course]= []

    @staticmethod
    def getCourse(order: int) -> Course | None:
        for course in CourseManager.courses:
            if(course.order == order):
                return course
        return None
    
    @staticmethod
    def getCoursesByTheoryCode(theoryCode: str) -> List[Course]:
        practiceClasses = []
        for course in CourseManager.courses:
            if(theoryCode != course.code and theoryCode in course.code):
                practiceClasses.append(course)
        return practiceClasses
        