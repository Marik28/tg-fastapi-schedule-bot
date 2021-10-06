import datetime
from typing import Optional

from pydantic import BaseModel

from .groups import Group, Subgroup
from .students import Student
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


class BaseStudentAssignment(BaseModel):
    assignment: Assignment
    student: Student
    done: bool


class StudentAssignment(BaseStudentAssignment):

    id: int

    class Config:
        orm_mode = True
