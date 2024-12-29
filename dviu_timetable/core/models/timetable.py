import datetime
from dataclasses import dataclass

from dviu_timetable.core.models.group import Group
from dviu_timetable.core.models.schedule import Schedule
from dviu_timetable.core.models.timetable_entry import TimetableEntry


@dataclass
class Timetable:
    timetable_id: int
    timetable_group: Group
    timetable_date: datetime.date
    timetable_schedule: Schedule
    timetable_entries: list[TimetableEntry]
