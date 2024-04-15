from app.course_repository import CourseRepository
from app.model import Course
from typing import List, Tuple, Dict, Set
from copy import deepcopy

# CourseRepository implementation that is coupled to the in-memory DB. A new implementation would be required if the database implementation changes
class CourseRepositoryImpl(CourseRepository):

    def __init__(self) -> None:
        self.database = Database()
        self.mapper = Mapper()
        super().__init__()

    def get_all_courses(self) -> List[Course]:
        all_course_entities = self.database.get_all()
        return list(map(lambda course_document: self.mapper.to_course_from_course_document(course_document), all_course_entities))

    def get_course(self, course_id: int) -> Course:
        return self.mapper.to_course_from_course_document(self.database.get(course_id))

    def save_course(self, course: Course) -> None:
        self.database.save(self.mapper.to_course_document_from_course(course))

    def delete_course(self, course_id: int) -> bool:
        try:
            self.database.delete(course_id)
            return True
        except:
            return False

# This class is used only for storage purposes in the DB
class CourseDocument:
    def __init__(self, id, name, students=None, assignments=None, submissions=None) -> None:
        self.id = id
        self.name = name
        self.students = students if students is not None else set()
        self.assignments = assignments if assignments is not None else dict()
        self.submissions = submissions if submissions is not None else dict()

# In-memory document oriented DB. Deep copy is used to ensure that callers do not modify DB directly
class Database():
    def __init__(self) -> None:
        self.courses = dict()

    def save(self, course_document: CourseDocument) -> None:
        self.courses.update(deepcopy({course_document.id: course_document}))

    def delete(self, id: int) -> None:
        del self.courses[id]

    def get(self, id: int) -> CourseDocument:
        return deepcopy(self.courses.get(id))
    
    def get_all(self) -> List[CourseDocument]:
        return deepcopy(list(self.courses.values()))

# Mapper that converts the in-memory DB documents to the models used by the application  
class Mapper():
    def __init__(self) -> None:
        pass

    def to_course_document_from_course(self, course: Course) -> CourseDocument:
        return CourseDocument(course.id, course.name, course.students, course.assignments, course.submissions)
    
    def to_course_from_course_document(self, course_document: CourseDocument) -> Course:
        return Course(course_document.id, course_document.name, course_document.students, course_document.assignments, course_document.submissions)

    