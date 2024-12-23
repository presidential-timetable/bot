import json
from pathlib import Path

from dviu_timetable.core.models.course import Course
from dviu_timetable.core.models.domain import Domain
from dviu_timetable.core.models.faculty import Faculty
from dviu_timetable.core.models.group import Group
from dviu_timetable.core.providers.abstract_group_provider import AbstractGroupProvider
from dviu_timetable.core.providers.abstract_domain_provider import AbstractDomainProvider
from dviu_timetable.core.providers.abstract_meta_provider import AbstractMetaProvider


class GroupProviderImpl(AbstractGroupProvider):
    def __init__(
            self,
            domain: Domain,
            domain_provider: AbstractDomainProvider,
            meta_provider: AbstractMetaProvider
    ) -> None:
        self._domain = domain
        self._domain_provider = domain_provider
        self._meta_provider = meta_provider
        self._groups_list = json.loads(
            Path('data/groups.json').read_text(encoding='utf-8')
        )

    def get_groups(
            self,
            course: Course | None = None,
            faculty: Faculty | None = None
    ) -> list[Group]:
        groups: list[Group] = [
            Group.get_from_dict(
                domain_provider=self._domain_provider,
                meta_provider=self._meta_provider,
                group_dict=group_dict
            )
            for group_dict in self._groups_list
            if group_dict['domain_id'] == self._domain.domain_id
        ]

        if course:
            groups = [
                group
                for group in groups
                if group.course.course_id == course.course_id
            ]

        if faculty:
            groups = [
                group
                for group in groups
                if group.faculty.faculty_id == faculty.faculty_id
            ]

        return groups

    def get_group_by_id(self, group_id: int) -> Group:
        for group in self.get_groups():
            if group.group_id == group_id:
                return group

        raise Exception(f'group {group_id} not found')
