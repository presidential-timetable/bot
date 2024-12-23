from abc import ABC, abstractmethod

from dviu_timetable.core.models.course import Course
from dviu_timetable.core.models.faculty import Faculty
from dviu_timetable.core.models.domain import Domain


class AbstractMetaProvider(ABC):
    @abstractmethod
    def __init__(self, domain: Domain) -> None:
        self._domain = domain

    @abstractmethod
    def get_courses(self) -> list[Course]:
        raise NotImplementedError

    @abstractmethod
    def get_course_by_id(self, course_id: int) -> Course:
        raise NotImplementedError

    @abstractmethod
    def get_faculties(self) -> list[Faculty]:
        raise NotImplementedError

    @abstractmethod
    def get_faculty_by_id(self, faculty_id: int) -> Faculty:
        raise NotImplementedError
