from app.course_service import CourseService
from app.model import Course
from typing import List
from app.course_repository import CourseRepository
from uuid import uuid4

class CourseServiceImpl(CourseService):
    
    def __init__(self, course_repository: CourseRepository) -> None:
        self.course_repository = course_repository
        super().__init__()

    def get_courses(self) -> List[Course]:
        return self.course_repository.get_all_courses()
    
    def get_course_by_id(self, course_id: int) -> Course:
        return self.course_repository.get_course(course_id)
    
    def create_course(self, course_name: str) -> int:
        new_course_id = uuid4().int
        course = Course(id=new_course_id, name=course_name)
        self.course_repository.save_course(course)
        return new_course_id
    
    def delete_course(self, course_id: int) -> bool:
        return self.course_repository.delete_course(course_id)
    
    def create_assignment(self, course_id: int, assignment_name: str) -> int:
        course = self.course_repository.get_course(course_id)
        new_assignment_id = course.create_assignment(assignment_name)
        self.course_repository.save_course(course)
        return new_assignment_id
    
    def enroll_student(self, course_id: int, student_id: int) -> bool:
        course = self.course_repository.get_course(course_id)
        enroll_succeeded = course.enroll_student(student_id)
        self.course_repository.save_course(course)
        return enroll_succeeded

    def dropout_student(self, course_id: int, student_id: int) -> bool:
        course = self.course_repository.get_course(course_id)
        dropout_succeeded = course.dropout_student(student_id)
        self.course_repository.save_course(course)
        return dropout_succeeded

    def submit_assignment(self, course_id: int, student_id: int, assignment_id: int, grade: int) -> bool:
        course = self.course_repository.get_course(course_id)
        submit_succeeded = course.submit_assignment(student_id, assignment_id, grade)
        self.course_repository.save_course(course)
        return submit_succeeded

    def get_assignment_grade_avg(self, course_id: int, assignment_id: int) -> int:
        course = self.course_repository.get_course(course_id)
        return course.get_assignment_grade_average(assignment_id)

    def get_student_grade_avg(self, course_id: int, student_id: int) -> int:
        course = self.course_repository.get_course(course_id)  
        return course.get_student_grade_average(student_id)

    def get_top_five_students(self, course_id: int) -> List[int]:
        course = self.course_repository.get_course(course_id)
        return course.get_top_five_students()