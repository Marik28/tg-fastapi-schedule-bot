from aiogram.dispatcher import FSMContext

from .api import fetch_assignments_list


async def get_assignments(state: FSMContext) -> str:
    user_data = await state.get_data()
    group = user_data.get("group")
    subgroup = user_data.get("subgroup")
    assignments = await fetch_assignments_list(group=group, subgroup=subgroup)

    if not assignments:
        return "Заданий нет"

    msg_bits = []
    for assignment in assignments:
        title = assignment.title
        is_important = '(Важно)' if assignment.is_important else ''
        msg_bits.append(f"-----------------------{title}{is_important}-----------------------")
        subject = assignment.subject.name
        date = assignment.complete_before.strftime('%d.%m')
        description = assignment.description or "-"
        msg_bits.append(f"Предмет - {subject}")
        msg_bits.append(f"Выполнить до {date}")
        msg_bits.append(f"Описание: {description}")

    return '\n'.join(msg_bits)
