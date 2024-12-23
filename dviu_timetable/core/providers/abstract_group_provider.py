from abc import ABC, abstractmethod

from dviu_timetable.core.models.course import Course
from dviu_timetable.core.models.faculty import Faculty
from dviu_timetable.core.models.domain import Domain
from dviu_timetable.core.models.group import Group


class AbstractGroupProvider(ABC):
    @abstractmethod
    def __init__(self, domain: Domain) -> None:
        self._domain = domain

    @abstractmethod
    def get_groups(self, course: Course, faculty: Faculty) -> list[Group]:
        raise NotImplementedError

    @abstractmethod
    def get_group_by_id(self, group_id: int) -> Group:
        raise NotImplementedError
