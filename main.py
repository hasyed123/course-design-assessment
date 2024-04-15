from app.course_service_impl import CourseServiceImpl
from app.course_repository_impl import CourseRepositoryImpl
import random

if __name__ == "__main__":
  course_service = CourseServiceImpl(CourseRepositoryImpl())

  course_id = course_service.create_course("Mathematics")
  students_to_enroll = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
  for student_id in students_to_enroll:
    course_service.enroll_student(course_id, student_id)

  assignment1_id = course_service.create_assignment(course_id, "math")
  assignment2_id = course_service.create_assignment(course_id, "science")
  
  for student_id in students_to_enroll:
    course_service.submit_assignment(course_id, student_id, assignment1_id, random.randint(0, 100))
    course_service.submit_assignment(course_id, student_id, assignment2_id, random.randint(0, 100))

  course = course_service.get_course_by_id(course_id)

  for student_id in students_to_enroll:
    print(course_service.get_student_grade_avg(course_id, student_id))

  print(course_service.get_assignment_grade_avg(course_id, assignment1_id))
  print(course_service.get_assignment_grade_avg(course_id, assignment2_id))
  print(course_service.get_top_five_students(course_id))

  pass
