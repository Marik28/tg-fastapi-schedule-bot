from aiogram.dispatcher import FSMContext
from aiogram.types import User
from loguru import logger

from .base import fetch, post, patch, put
from ..models.assignments import StudentAssignment
from ..models.students import StudentCreate
from ..services.fsm import get_group_and_subgroup
from ..settings import settings


async def fetch_student_assignments(telegram_user: User, done: bool = False) -> list[StudentAssignment]:
    query = {
        "done": str(done),
    }
    student_assignments = await fetch(
        settings.student_assignments_endpoint.format(student_id=telegram_user.id, assignment_id=""), query
    )
    return [StudentAssignment.parse_obj(student_assignment) for student_assignment in student_assignments]


async def register_or_update(telegram_user: User, state: FSMContext) -> None:
    group, subgroup = await get_group_and_subgroup(state)
    student_data = StudentCreate(group_name=group, subgroup=str(subgroup), telegram_id=telegram_user.id).dict()
    response = await post(settings.students_endpoint, data=student_data)
    logger.debug(student_data)
    if response.status == 409:
        await put(settings.students_endpoint + f"{telegram_user.id}", data=student_data)


async def mark_completed(telegram_user: User, done: bool, assignments_id: int):
    data = {
        "done": done,
    }
    response = await patch(
        settings.student_assignments_endpoint.format(student_id=telegram_user.id, assignment_id=assignments_id), data)
    logger.debug(response.status)
