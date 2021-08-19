from pydantic import BaseModel, Field


class BaseTeacher(BaseModel):
    """Модель, описывающая преподавателя"""
    first_name: str = Field(..., description="Имя преподавателя")
    second_name: str = Field(..., description="Фамилия преподавателя")
    middle_name: str = Field(..., description="Отчество преподавателя")


class Teacher(BaseTeacher):
    id: int

    class Config:
        orm_mode = True
