from app.course_repository import CourseRepository
from app.model import Course
from app.entity import CourseEntity
from typing import List, Tuple, Dict, Set
from copy import deepcopy

# CourseRepository that is coupled to the in-memory DB. A new implementation would be required if the database implementation changes
class CourseRepositoryImpl(CourseRepository):

    def __init__(self) -> None:
        self.database = Database()
        self.mapper = Mapper()
        super().__init__()

    def get_all_courses(self) -> List[Course]:
        all_course_entities = self.database.get_all()
        return list(map(lambda course_entity: self.mapper.to_course_from_course_entity(course_entity), all_course_entities))

    def get_course(self, course_id: int) -> Course:
        return self.mapper.to_course_from_course_entity(self.database.get(course_id))

    def save_course(self, course: Course) -> None:
        self.database.save(self.mapper.to_course_entity_from_course(course))

    def delete_course(self, course_id: int) -> None:
        self.database.delete(course_id)

# In-memory document oriented DB. Deep copy is used to ensure that callers do not modify DB directly
class Database():
    def __init__(self) -> None:
        self.courses = dict()

    def save(self, course_entity: CourseEntity) -> None:
        self.courses.update(deepcopy({course_entity.id: course_entity}))

    def delete(self, id: int) -> None:
        del self.courses[id]

    def get(self, id: int) -> CourseEntity:
        return deepcopy(self.courses.get(id))
    
    def get_all(self) -> List[CourseEntity]:
        return deepcopy(list(self.courses.values()))

# Mapper that converts the in-memory DB data structures to the models used by the application  
class Mapper():
    def __init__(self) -> None:
        pass

    def to_course_entity_from_course(self, course: Course) -> CourseEntity:
        return CourseEntity(course.id, course.name, course.students, course.assignments, course.submissions)
    
    def to_course_from_course_entity(self, course_entity: CourseEntity) -> Course:
        return Course(course_entity.id, course_entity.name, course_entity.students, course_entity.assignments, course_entity.submissions)

    