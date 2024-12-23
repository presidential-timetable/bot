from __future__ import annotations

from dataclasses import dataclass

from dviu_timetable.core.providers.abstract_domain_provider import AbstractDomainProvider
from dviu_timetable.core.models.domain import Domain


@dataclass
class Course:
    course_domain: Domain
    course_id: int
    course_name: str

    @classmethod
    def get_from_dict(cls, domain_provider: AbstractDomainProvider, course_dict: dict) -> Course:
        return Course(
            course_domain=domain_provider.get_domain_by_id(course_dict['domain_id']),
            course_id=course_dict['course_id'],
            course_name=course_dict['course_name']
        )
