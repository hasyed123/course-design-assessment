from uuid import uuid4
from typing import List
import math

'''
This class is a data structure that stores course information
and encapsulates the business logic around modifying that data and performing calculations on it.
Keeping this logic here ensures the integrity of the data
'''
class Course:
    def __init__(self, id, name, students=None, assignments=None, submissions=None) -> None:
        if not name:
            raise ValueError("Name must be present")
        self.id = id
        self.name = name
        self.students = students if students is not None else set()
        self.assignments = assignments if assignments is not None else dict()
        self.submissions = submissions if submissions is not None else dict()

    def create_assignment(self, assignment_name) -> int:
        if not assignment_name:
            raise ValueError("Name must be present")
        new_assignment_id = uuid4().int
        self.assignments.update({new_assignment_id: assignment_name})
        return new_assignment_id
    
    def enroll_student(self, student_id) -> bool:
        if student_id in self.students:
            return False
        self.students.add(student_id)
        return True

    def dropout_student(self, student_id) -> bool:
        if student_id not in self.students:
            return False
        self.students.discard(student_id)
        return True
    
    def submit_assignment(self, student_id, assignment_id, grade) -> bool:
        if student_id not in self.students or assignment_id not in self.assignments:
            return False
        if (student_id, assignment_id) in self.submissions:
            return False
        if grade < 0 or grade > 100:
            return False
        self.submissions.update({(student_id, assignment_id) : grade})
        return True

    def get_assignment_grade_average(self, assignment_id) -> int:
        if assignment_id not in self.assignments:
            raise Exception(f"Assignment {assignment_id} does not exist in course {self.id}!")
        submissions_of_assignment = [el[1] for el in self.submissions.items() if assignment_id in el[0]]
        if not submissions_of_assignment:
            raise Exception(f"Assignment {assignment_id} has no submissions in course {self.id}!")
        return math.floor(sum(submissions_of_assignment) / len(submissions_of_assignment))
        
    def get_student_grade_average(self, student_id) -> int:
        if student_id not in self.students:
            raise Exception(f"Student {student_id} does not exist in course {self.id}!")
        submissions_of_student = [el[1] for el in self.submissions.items() if student_id in el[0]]
        if not submissions_of_student:
            raise Exception(f"Student {student_id} has not submitted assignments in course {self.id}!")
        return math.floor(sum(submissions_of_student) / len(submissions_of_student))
    
    def get_top_five_students(self) -> List[int]:
        student_averages = {}
        for student_id in self.students:
            try:
                student_averages[student_id] = self.get_student_grade_average(student_id)
            except:
                pass
        return sorted(student_averages, key=student_averages.get, reverse=True)[:5]
    
