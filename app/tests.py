import unittest
from model import Course

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

    def test_enroll_student_with_no_id(self):
        with self.assertRaises(TypeError):
            self.course.enroll_student(None)

    def test_enroll_student_when_student_already_enrolled(self):
        student_id = 100
        self.add_student(student_id)

        succeed = self.course.enroll_student(student_id)

        self.assertIn(student_id, self.course.students)
        self.assertFalse(succeed)

    def test_submit_assignment(self):
        student_id = 100
        assignment_id = 1000
        self.add_student(student_id)
        self.add_assignment(assignment_id, "assignment name")
        grade = 95

        succeed = self.course.submit_assignment(student_id, assignment_id, 95)

        self.assertIn((student_id, assignment_id), self.course.submissions)
        self.assertTrue(succeed)


    # helper methods to populate data for tests

    def add_student(self, student_id):
        self.course.students.add(student_id)
    
    def add_assignment(self, assignment_id, name):
        self.course.assignments.update({assignment_id: name})

    def add_assignment_submission(self, student_id, assignment_id, grade):
        self.course.submissions.update({(student_id, assignment_id): grade})
        
if __name__ == '__main__':
    unittest.main()