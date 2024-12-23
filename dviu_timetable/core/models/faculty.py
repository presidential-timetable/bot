from __future__ import annotations

from dataclasses import dataclass

from dviu_timetable.core.models.domain import Domain
from dviu_timetable.core.providers.abstract_domain_provider import AbstractDomainProvider


@dataclass
class Faculty:
    faculty_domain: Domain
    faculty_id: int
    faculty_name: str

    @classmethod
    def get_from_dict(cls, domain_provider: AbstractDomainProvider, faculty_dict: dict) -> Faculty:
        return Faculty(
            faculty_domain=domain_provider.get_domain_by_id(faculty_dict['domain_id']),
            faculty_id=faculty_dict['faculty_id'],
            faculty_name=faculty_dict['faculty_name']
        )
