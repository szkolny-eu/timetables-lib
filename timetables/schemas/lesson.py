from datetime import time
from typing import List, Optional

from pydantic import Field

from ..base import Identifiable
from .classroom import Classroom
from .register import Register
from .subject import Subject
from .teacher import Teacher
from .team import Team
from .weekday import WeekDay


class Lesson(Identifiable):
    weekday: WeekDay = Field(title="Weekday", description="Weekday of the lesson")
    number: Optional[int] = Field(
        None, title="Lesson Number", description="The lesson range number"
    )
    time_start: time = Field(title="Start Time", description="Start time of the lesson")
    time_end: Optional[time] = Field(
        None, title="End Time", description="End time of the lesson, if available"
    )
    register_: Register = Field(
        None, title="Register", description="A register in which this lesson is added"
    )
    team: Optional[Team] = Field(
        None, title="Team", description="A part of the register having this lesson"
    )
    subject: Subject = Field(
        title="Subject", description="The school subject of the lesson"
    )
    teachers: List[Teacher] = Field(
        title="Teachers", description="A list of teachers assigned to this lesson"
    )
    classroom: Optional[Classroom] = Field(
        title="Classroom", description="The classroom where this lesson takes place"
    )

    def __hash__(self) -> int:
        return self.internal_id

    def __str__(self) -> str:
        return (
            f"Lesson("
            f"internal_id={self.internal_id}, "
            f"weekday={self.weekday.name}, "
            f"number={self.number}, "
            f"time_start={self.time_start.strftime('%H:%M')}, "
            f"time_end={self.time_end.strftime('%H:%M') if self.time_end else None}, "
            f"register='{self.register_.name}', "
            f"team='{self.team.name if self.team else None}', "
            f"subject='{self.subject.name}', "
            f"teachers={list(t.name for t in self.teachers)}, "
            f"classroom='{self.classroom.name if self.classroom else None}')"
        )
