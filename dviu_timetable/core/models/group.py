from __future__ import annotations

from dataclasses import dataclass

from dviu_timetable.core.models.domain import Domain
from dviu_timetable.core.models.faculty import Faculty
from dviu_timetable.core.models.course import Course
from dviu_timetable.core.providers.abstract_domain_provider import AbstractDomainProvider
from dviu_timetable.core.providers.abstract_meta_provider import AbstractMetaProvider


@dataclass
class Group:
    group_id: int
    domain: Domain
    faculty: Faculty
    course: Course
    group_name: str

    @classmethod
    def get_from_dict(
            cls,
            domain_provider: AbstractDomainProvider,
            meta_provider: AbstractMetaProvider,
            group_dict: dict
    ) -> Group:
        domain = domain_provider.get_domain_by_id(group_dict['domain_id'])
        faculty = meta_provider.get_faculty_by_id(group_dict['faculty_id'])
        course = meta_provider.get_course_by_id(group_dict['course_id'])

        return Group(
            group_id=group_dict['group_id'],
            domain=domain,
            faculty=faculty,
            course=course,
            group_name=group_dict['group']
        )
