from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from zoneinfo import ZoneInfo

from dviu_timetable.core.models.course import Course
from dviu_timetable.core.models.domain import Domain
from dviu_timetable.core.models.faculty import Faculty
from dviu_timetable.core.models.group import Group

from dviu_timetable.core.database.connector import connection


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
    def _build_from_tuple(cls, data: tuple) -> User:
        ...  # TODO

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
    def get_by_id(cls, user_id: int) -> User:
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM users WHERE user_id = ?', user_id)
        data = cursor.fetchone()
        if not data:
            raise Exception(f'user with id {user_id} not found')

        return data
