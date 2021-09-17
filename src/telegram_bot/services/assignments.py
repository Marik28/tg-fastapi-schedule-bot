from aiogram.dispatcher import FSMContext
from aiogram.utils.markdown import hbold

from ..api.assignments import fetch_assignments_list
from ..models import Assignment


async def get_assignments(state: FSMContext) -> str:
    user_data = await state.get_data()
    group = user_data.get("group")
    subgroup = user_data.get("subgroup")
    assignments = await fetch_assignments_list(group=group, subgroup=subgroup)

    return render_assignments(assignments)


def render_assignments(assignments: list[Assignment]) -> str:
    if not assignments:
        return "Заданий нет"

    msg_bits = []
    for assignment in assignments:
        title = assignment.title
        is_important = '(Важно)' if assignment.is_important else ''
        msg_bits.append(
            f"{'❗' if is_important else ''}{hbold(title)} {hbold(is_important)}{'❗' if is_important else ''}")
        subject = assignment.subject.name
        date = assignment.complete_before.strftime('%d.%m')
        description = assignment.description
        msg_bits.append(f"📝 Предмет - {subject}")
        msg_bits.append(f"📅 Выполнить до {date}")
        if description:
            msg_bits.append(f"Описание: {description}")
        msg_bits.append("------------------------------")

    return '\n'.join(msg_bits)
