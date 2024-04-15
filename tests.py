import unittest
from app.model import Course
from unittest.mock import MagicMock
from app.course_repository import CourseRepository
from app.course_service_impl import CourseServiceImpl

class TestCourse(unittest.TestCase):
    def setUp(self) -> None:
        self.course = Course(id=1, name="Test Course")

    def test_create_assignment(self):
        assignment_id = self.course.create_assignment("Assignment 1")

        self.assertIn(assignment_id, self.course.assignments)
        self.assertEqual(self.course.assignments[assignment_id], "Assignment 1")

    def test_create_assignment_with_empty_name(self):
        with self.assertRaises(ValueError):
            self.course.create_assignment("")

    def test_enroll_student(self):
        student_id = 100

        succeed = self.course.enroll_student(student_id)

        self.assertIn(student_id, self.course.students)
        self.assertTrue(succeed)

    def test_enroll_student_when_student_already_enrolled(self):
        student_id = 100
        self.add_student(student_id)

        succeed = self.course.enroll_student(student_id)

        self.assertIn(student_id, self.course.students)
        self.assertFalse(succeed)

    def test_dropout_student(self):
        student_id = 100
        self.add_student(student_id)

        succeed = self.course.dropout_student(student_id)

        self.assertNotIn(student_id, self.course.students)
        self.assertTrue(succeed)

    def test_dropout_student_when_student_is_not_enrolled(self):
        student_id = 100

        self.assertFalse(self.course.dropout_student(student_id))

    def test_submit_assignment(self):
        student_id = 100
        assignment_id = 1000
        self.add_student(student_id)
        self.add_assignment(assignment_id, "assignment name")
        grade = 95

        succeed = self.course.submit_assignment(student_id, assignment_id, grade)

        self.assertIn((student_id, assignment_id), self.course.submissions)
        self.assertTrue(succeed)

    def test_submit_assignment_with_grade_below_0(self):
        student_id = 100
        assignment_id = 1000
        self.add_student(student_id)
        self.add_assignment(assignment_id, "assignment name")
        grade = -1

        succeed = self.course.submit_assignment(student_id, assignment_id, grade)

        self.assertNotIn((student_id, assignment_id), self.course.submissions)
        self.assertFalse(succeed)

    def test_submit_assignment_when_grade_above_100(self):
        student_id = 100
        assignment_id = 1000
        self.add_student(student_id)
        self.add_assignment(assignment_id, "assignment name")
        grade = 105

        succeed = self.course.submit_assignment(student_id, assignment_id, grade)

        self.assertNotIn((student_id, assignment_id), self.course.submissions)
        self.assertFalse(succeed)

    def test_get_assignment_grade_average(self):
        student_id_1 = 100
        student_id_2 = 200
        assignment_id = 1000
        grade1 = 60
        grade2 = 63
        self.add_student(student_id_1)
        self.add_student(student_id_2)
        self.add_assignment(assignment_id, "Name")
        self.add_assignment_submission(student_id_1, assignment_id, grade1)
        self.add_assignment_submission(student_id_2, assignment_id, grade2)

        self.assertEqual(61, self.course.get_assignment_grade_average(assignment_id))

    def test_get_assignment_grade_average_when_assignment_does_not_exist(self):
        with self.assertRaises(Exception):
            self.course.get_assignment_grade_average(1000)

    def test_get_assignment_grade_average_when_assignment_has_no_submissions(self):
        assignment_id = 1000
        self.add_assignment(assignment_id, "Name")

        with self.assertRaises(Exception):
            self.course.get_assignment_grade_average(assignment_id)

    def test_get_student_grade_average(self):
        student_id = 100
        assignment_1_id = 1000
        assignment_2_id = 2000
        grade1 = 70
        grade2 = 81
        self.add_student(student_id)
        self.add_assignment(assignment_1_id, "Name")
        self.add_assignment(assignment_2_id, "Name")
        self.add_assignment_submission(student_id, assignment_1_id, grade1)
        self.add_assignment_submission(student_id, assignment_2_id, grade2)

        self.assertEqual(75, self.course.get_student_grade_average(student_id))

    def test_get_student_grade_average_when_student_does_not_exist(self):
        with self.assertRaises(Exception):
            self.course.get_student_grade_average(100)

    def test_get_student_grade_average_when_student_has_no_submissions(self):
        student_id = 100
        self.add_student(student_id)

        with self.assertRaises(Exception):
            self.course.get_student_grade_average(student_id)

    def test_get_top_five_students(self):
        student_ids = [100, 200, 300, 400, 500, 600, 700, 800, 900]
        assignment_ids = [1000, 2000]
        for student_id in student_ids:
            self.add_student(student_id)
        for assignment_id in assignment_ids:
            self.add_assignment(assignment_id, "Name")
        for student_id in student_ids:
            for assignment_id in assignment_ids:
                self.add_assignment_submission(student_id, assignment_id, student_id/10)

        top_five_students = self.course.get_top_five_students()

        self.assertEqual([900, 800, 700, 600, 500], top_five_students)

    # helper methods to populate data for tests

    def add_student(self, student_id):
        self.course.students.add(student_id)
    
    def add_assignment(self, assignment_id, name):
        self.course.assignments.update({assignment_id: name})

    def add_assignment_submission(self, student_id, assignment_id, grade):
        self.course.submissions.update({(student_id, assignment_id): grade})

class TestCourseServiceImpl(unittest.TestCase):
    def setUp(self) -> None:
        self.course_repository_mock = MagicMock(spec=CourseRepository)
        self.course_service = CourseServiceImpl(self.course_repository_mock)
        self.course_mock = MagicMock(spec=Course)
        self.course_repository_mock.get_course.return_value = self.course_mock
        self.course_repository_mock.get_all_courses.return_value = [self.course_mock]

    def test_get_courses(self):
        courses = self.course_service.get_courses()

        self.assertEqual([self.course_mock], courses)

    def test_get_course(self):
        course = self.course_service.get_course_by_id(1)

        self.assertEqual(self.course_mock, course)

    def test_create_course(self):
        new_course_id = self.course_service.create_course("New Course")

        self.assertIsNotNone(new_course_id)
        self.course_repository_mock.save_course.assert_called_once()

    def test_create_assignment(self):
        self.course_mock.create_assignment.return_value = 1

        new_assignment_id = self.course_service.create_assignment(1, "New assignment")

        self.assertEqual(1, new_assignment_id)
        self.course_repository_mock.save_course.assert_called_once()

    def test_enroll_student(self):
        self.course_service.enroll_student(1, 100)

        self.course_repository_mock.save_course.assert_called_once()

    def test_dropout_student(self):
        self.course_service.dropout_student(1, 100)

        self.course_repository_mock.save_course.assert_called_once()

    def test_submit_assignment(self):
        self.course_service.submit_assignment(1, 100, 1000, 80)

        self.course_repository_mock.save_course.assert_called_once()

    def test_get_assignment_grade_avg(self):
        self.course_mock.get_assignment_grade_average.return_value = 90

        self.assertEqual(90, self.course_service.get_assignment_grade_avg(1, 1000))

    def test_get_student_grade_avg(self):
        self.course_mock.get_student_grade_average.return_value = 90

        self.assertEqual(90, self.course_service.get_student_grade_avg(1, 1000))

    def test_get_top_five_students(self):
        self.course_mock.get_top_five_students.return_value = [3, 4, 5, 6, 7]

        self.assertEqual([3, 4, 5, 6, 7], self.course_service.get_top_five_students(1))
        
if __name__ == '__main__':
    unittest.main()