import json
from pathlib import Path

from dviu_timetable.core.providers.abstract_meta_provider import AbstractMetaProvider
from dviu_timetable.core.providers.abstract_domain_provider import AbstractDomainProvider

from dviu_timetable.core.models.course import Course
from dviu_timetable.core.models.faculty import Faculty
from dviu_timetable.core.models.domain import Domain


class MetaProviderImpl(AbstractMetaProvider):
    def __init__(self, domain: Domain, domain_provider: AbstractDomainProvider):
        self._domain = domain
        self._domain_provider = domain_provider
        self._courses_list = json.loads(
            Path('data/courses.json').read_text(encoding='utf-8')
        )
        self._faculties_list = json.loads(
            Path('data/faculties.json').read_text(encoding='utf-8')
        )

    # Courses

    def get_courses(self) -> list[Course]:
        return [
            Course.get_from_dict(
                self._domain_provider, course_dict
            ) for course_dict in self._courses_list
            if course_dict['domain_id'] == self._domain.domain_id
        ]

    def get_course_by_id(self, course_id: int) -> Course:
        for course in self.get_courses():
            if course.course_id == course_id:
                return course

        raise Exception(f'course {course_id} not found')

    # Faculties

    def get_faculties(self) -> list[Faculty]:
        return [
            Faculty.get_from_dict(
                self._domain_provider, faculty_dict
            ) for faculty_dict in self._faculties_list
            if faculty_dict['domain_id'] == self._domain.domain_id
        ]

    def get_faculty_by_id(self, faculty_id: int) -> Faculty:
        for faculty in self.get_faculties():
            if faculty.faculty_id == faculty_id:
                return faculty

        raise Exception(f'faculty {faculty_id} not found')
