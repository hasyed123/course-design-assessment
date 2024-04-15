from app.course_service_impl import CourseServiceImpl
from app.course_repository_impl import CourseRepositoryImpl
import random

if __name__ == "__main__":
    course_service = CourseServiceImpl(CourseRepositoryImpl())
    # Create a single course
    course_name = "Course 1"
    course_id = course_service.create_course(course_name)
    print(f"Created course: {course_name} with ID: {course_id}")

    number_of_students = 6
    number_of_assignments = 4

    # Enroll students
    for student_id in range(number_of_students):
        enroll_succeeded = course_service.enroll_student(course_id, student_id)
        print(f"Enrolled student {student_id}: {enroll_succeeded}")

    # Create assignments
    assignment_ids = {}
    for assignment_id in range(number_of_assignments):
        assignment_name = f"Assignment {assignment_id}"
        new_assignment_id = course_service.create_assignment(course_id, assignment_name)
        assignment_ids.update({new_assignment_id: assignment_name})
        print(f"Created assignment: {assignment_name} with ID: {new_assignment_id}")

    # Submit assignments with random grades between 0 and 100
    for student_id in range(number_of_students):
        for assignment_id in assignment_ids:
            grade = random.randint(0, 100)
            submit_succeeded = course_service.submit_assignment(course_id, student_id, assignment_id, grade)
            print(f"Submitted assignment {assignment_ids.get(assignment_id)} for student {student_id} with grade {grade}: {submit_succeeded}")

    # Display average grade of each assignment
    for assignment_id in assignment_ids:
        avg_grade = course_service.get_assignment_grade_avg(course_id, assignment_id)
        print(f"Average grade for assignment {assignment_ids.get(assignment_id)}: {avg_grade}")

    # Display average grade of each student
    for student_id in range(number_of_students):
        avg_grade = course_service.get_student_grade_avg(course_id, student_id)
        print(f"Average grade for student {student_id}: {avg_grade}")

    # Display top five students
    top_students = course_service.get_top_five_students(course_id)
    print(f"Top five students in course {course_id}: {top_students}")

    # Create another course
    course_name_2 = "Course 2"
    course_id_2 = course_service.create_course(course_name)
    print(f"Created course: {course_name_2} with ID: {course_id_2}")

    # Display all courses
    all_courses = course_service.get_courses()
    print(f"All courses: {list(map(lambda course: course.id, all_courses))}")

    # Delete both courses
    delete_succeeded = course_service.delete_course(course_id)
    print(f"Deleted course id {course_id}: {delete_succeeded}")
    delete_succeeded = course_service.delete_course(course_id_2)
    print(f"Deleted course id {course_id_2}: {delete_succeeded}")

    # Display all courses
    all_courses = course_service.get_courses()
    print(f"All courses: {list(map(lambda course: course.id, all_courses))}")