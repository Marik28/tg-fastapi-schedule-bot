from typing import Optional

from pydantic import BaseModel, Field


class BaseUsefulLink(BaseModel):
    link: str
    description: Optional[str]


class UsefulLink(BaseUsefulLink):
    id: int

    class Config:
        orm_mode = True


class BaseSubject(BaseModel):
    """Модель, описывающая предмет"""
    name: str = Field(..., description="Название предмета")


class LessonSubject(BaseSubject):
    id: int

    class Config:
        orm_mode = True


class Subject(LessonSubject):
    useful_links: Optional[list[UsefulLink]]
