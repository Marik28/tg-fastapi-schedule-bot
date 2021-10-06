from aiogram.dispatcher import FSMContext
from aiogram.types import User
from aiogram.utils.markdown import hbold

from .fsm import get_group_and_subgroup
from ..api.assignments import fetch_assignments_list
from ..api.students import fetch_student_assignments
from ..models import Assignment


async def get_assignments(state: FSMContext) -> str:
    group, subgroup = await get_group_and_subgroup(state)
    assignments = await fetch_assignments_list(group=group, subgroup=subgroup)

    return render_assignments(assignments)


async def get_student_assignments(user: User, done: bool = False) -> str:
    assignments = await fetch_student_assignments(telegram_user=user, done=done)
    return render_assignments([assignment.assignment for assignment in assignments], add_completion=True, done=done)


def render_assignments(assignments: list[Assignment], add_completion: bool = False, done: bool = False) -> str:
    if not assignments:
        return "Заданий нет"

    msg_bits = []
    for assignment in assignments:
        title = assignment.title

        if add_completion:
            if done:
                first_part = "/uncomplete"
            else:
                first_part = "/complete"
            completion_part = f"{first_part}_{assignment.id}"
        else:
            completion_part = ""

        is_important = '(Важно)' if assignment.is_important else ''
        msg_bits.append(
            f"{'❗' if is_important else ''}"
            f"{hbold(title)}"
            f" {hbold(is_important)}"
            f"{'❗' if is_important else ''}"
            f"{completion_part}"
        )
        subject = assignment.subject.name
        date = assignment.complete_before.strftime('%d.%m')
        description = assignment.description
        msg_bits.append(f"📝 Предмет - {subject}")
        msg_bits.append(f"📅 Выполнить до {date}")
        if description:
            msg_bits.append(f"Описание: {description}")
        msg_bits.append("------------------------------")

    return '\n'.join(msg_bits)
