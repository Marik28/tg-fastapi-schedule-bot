import datetime as dt
from enum import Enum, IntEnum
from typing import Optional

from pydantic import BaseModel, Field

from .groups import Group, Subgroup
from .subjects import LessonSubject
from .teachers import Teacher


class Building(IntEnum):
    """Перечисление корпусов университета"""
    MAIN = 0
    FIRST = 1
    SECOND = 2
    THIRD = 3
    FOURTH = 4


class BaseClassRoom(BaseModel):
    """Модель, описывающая аудиторию"""
    number: int = Field(..., description="Номер аудитории")
    building: Building = Field(..., description="Корпус университета, в котором находится аудитория")


class ClassRoom(BaseClassRoom):
    id: int

    class Config:
        orm_mode = True


class WeekDay(IntEnum):
    """Перечисления дней недели"""
    MONDAY = 1
    TUESDAY = 2
    WEDNESDAY = 3
    THURSDAY = 4
    FRIDAY = 5
    SATURDAY = 6
    SUNDAY = 7


class Parity(IntEnum):
    """Перечисление вариантов четности пары (числитель, знаменатель или всегда)"""
    NUMERATOR = 1
    DENOMINATOR = 2
    ALWAYS = 3


class LessonKind(str, Enum):
    """Перечисление типов пары"""
    LECTURE = 'Лекция'
    LAB = 'Лабораторное занятие'
    SEMINAR = 'Семинар'
    SRSP = 'СРСП'
    SRS = 'СРС'
    CURATORIAL_HOUR = 'Кураторский час'


class BaseLesson(BaseModel):
    """Модель, описывающая пару"""
    subject: LessonSubject = Field(..., description="Предмет, по которому проходит пара")
    teacher: Teacher = Field(..., description="Преподаватель, который ведет пару")
    classroom: Optional[ClassRoom] = Field(None, description="Аудитория, в которой проходит пара")
    group: Group = Field(..., description="Группа, у которой проходит пара")
    subgroup: Subgroup = Field(..., description="Подгруппа, у которой проходит пара")
    kind: LessonKind = Field(..., description="Тип занятия")
    day: WeekDay = Field(..., description="День недели, в который проходит пара, в виде перечисления")
    parity: Parity = Field(..., description="Четность недели, в которую проходит пара")
    time: dt.time = Field(..., description="Время прохождения пары")


class Lesson(BaseLesson):
    id: int

    class Config:
        orm_mode = True
