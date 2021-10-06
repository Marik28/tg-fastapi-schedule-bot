from enum import Enum

from pydantic import BaseModel, Field


class BaseGroup(BaseModel):
    """Модель, описывающая группу"""
    name: str = Field(..., description="Название группы")


class Group(BaseGroup):
    id: int

    class Config:
        orm_mode = True


class Subgroup(str, Enum):
    """Перечисления подгрупп"""
    FIRST_GROUP = "1"
    SECOND_GROUP = "2"
    BOTH = "3"
