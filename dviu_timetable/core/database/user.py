from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from zoneinfo import ZoneInfo

from dviu_timetable.core.models.course import Course
from dviu_timetable.core.models.domain import Domain
from dviu_timetable.core.models.faculty import Faculty
from dviu_timetable.core.models.group import Group

from dviu_timetable.core.database.connector import connection
from dviu_timetable.core.providers.abstract_domain_provider import AbstractDomainProvider
from dviu_timetable.core.providers.abstract_group_provider import AbstractGroupProvider
from dviu_timetable.core.providers.abstract_meta_provider import AbstractMetaProvider


@dataclass
class User:
    user_id: int
    telegram_name: str
    telegram_username: str | None
    name: str
    activated_on: datetime
    role: str
    domain: Domain
    faculty: Faculty
    course: Course
    group: Group

    @classmethod
    def _build_from_tuple(
            cls,
            data: tuple,
            domain_provider: AbstractDomainProvider,
            meta_provider: AbstractMetaProvider,
            group_provider: AbstractGroupProvider
    ) -> User:
        return User(
            user_id=data[0],
            telegram_name=data[1],
            telegram_username=data[2],
            name=data[3],
            activated_on=datetime.fromisoformat(data[4]),
            role=data[5],
            domain=domain_provider.get_domain_by_id(data[6]),
            faculty=meta_provider.get_faculty_by_id(data[7]),
            course=meta_provider.get_course_by_id(data[8]),
            group=group_provider.get_group_by_id(data[9])
        )

    @classmethod
    def create(
            cls,
            *,
            user_id: int,
            telegram_name: str,
            name: str,
            role: str,
            domain: Domain,
            faculty: Faculty,
            course: Course,
            group: Group,
            telegram_username: str | None
    ) -> User:
        activated_on = datetime.now(ZoneInfo('Asia/Vladivostok'))
        cursor = connection.cursor()
        cursor.execute(
            f"INSERT INTO users VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (user_id,
            telegram_name,
            telegram_username,
            name,
            activated_on,
            role,
            domain.domain_id,
            faculty.faculty_id,
            course.course_id,
            group.group_id)
        )
        connection.commit()
        return User(
            user_id, telegram_name, telegram_username, name, activated_on, role, domain, faculty, course, group
        )

    @classmethod
    def get_by_id(
            cls,
            user_id: int,
            domain_provider: AbstractDomainProvider,
            meta_provider: AbstractMetaProvider,
            group_provider: AbstractGroupProvider
    ) -> User:
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM users WHERE user_id = ?;', (user_id,))
        data = cursor.fetchone()
        if not data:
            raise Exception(f'user with id {user_id} not found')

        return cls._build_from_tuple(data, domain_provider, meta_provider, group_provider)

    @classmethod
    def check_exists(cls, user_id: int) -> bool:
        """For contexts where all the providers are not initialized yet"""
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM users WHERE user_id = ?;', (user_id,))
        data = cursor.fetchone()
        return bool(data)

    @classmethod
    def get_dict_data_by_id(cls, user_id: int) -> dict[str, str|int]:
        """For example, to initialize providers by id"""
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM users WHERE user_id = ?;', (user_id,))
        data = cursor.fetchone()
        if not data:
            raise Exception(f'user with id {user_id} not found')

        return {
            'user_id': data[0],
            'telegram_name': data[1],
            'telegram_username': data[2],
            'name': data[3],
            'activated_on': datetime.fromisoformat(data[4]),
            'role': data[5],
            'domain_id': data[6],
            'faculty_id': data[7],
            'course_id': data[8],
            'group_id': data[9]
        }
