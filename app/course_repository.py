from abc import ABC, abstractmethod
from typing import List
from app.model import Course


class CourseRepository(ABC):
    @abstractmethod
    def get_all_courses(self) -> List[Course]:
        """
        Returns a list of all courses.
        """
        pass

    @abstractmethod
    def get_course(self, course_id) -> Course:
        """
        Returns a course by its id.
        """
        pass

    @abstractmethod
    def save_course(self, course) -> None:
        pass

    @abstractmethod
    def delete_course(self, course_id) -> None:
        pass