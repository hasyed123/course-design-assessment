from abc import ABC, abstractmethod
from typing import List
from app.model import Course

# Repository interface that abstracts the persistence logic from the rest of the app. 
# This allows for the possibility of replacing the db without affecting the rest of the app
class CourseRepository(ABC):
    @abstractmethod
    def get_all_courses(self) -> List[Course]:
        pass

    @abstractmethod
    def get_course(self, course_id: int) -> Course:
        pass

    @abstractmethod
    def save_course(self, course: Course) -> None:
        pass

    @abstractmethod
    def delete_course(self, course_id: int) -> bool:
        pass