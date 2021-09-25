import datetime
from typing import Optional

from pydantic import BaseModel

from .groups import Group, Subgroup
from .subjects import LessonSubject


class BaseAssignments(BaseModel):
    subject: LessonSubject
    complete_before: datetime.date
    description: Optional[str]
    title: str
    is_important: bool
    archived: bool
    group: Group
    subgroup: Subgroup


class Assignment(BaseAssignments):
    id: int

    class Config:
        orm_mode = True
