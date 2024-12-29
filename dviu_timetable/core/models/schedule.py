from dataclasses import dataclass

from dviu_timetable.core.models.domain import Domain
from dviu_timetable.core.models.schedule_block import ScheduleBlock


@dataclass
class Schedule:
    schedule_id: int
    domain: Domain
    blocks: list[ScheduleBlock]
