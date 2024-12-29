import datetime
from dataclasses import dataclass


@dataclass
class ScheduleBlock:
    lesson_id: int
    start_time: datetime.time
    end_time: datetime.time
    break_duration_min: int
