from pydantic import BaseModel

from .groups import Group, Subgroup


class BaseStudent(BaseModel):
    telegram_id: int
    subgroup: Subgroup


class StudentCreate(BaseStudent):
    group_name: str

    class Config:
        use_enum_values = True


class StudentUpdate(BaseModel):
    group_name: str
    subgroup: Subgroup


class Student(BaseStudent):
    group: Group

    class Config:
        orm_mode = True
