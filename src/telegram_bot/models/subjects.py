from pydantic import BaseModel, Field


class BaseSubject(BaseModel):
    """Модель, описывающая предмет"""
    name: str = Field(..., description="Название предмета")


class Subject(BaseSubject):
    id: int

    class Config:
        orm_mode = True
