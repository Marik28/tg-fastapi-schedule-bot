from aiogram.dispatcher import FSMContext

from ..api.assignments import fetch_assignments_list
from .rendering import render_assignments


async def get_assignments(state: FSMContext) -> str:
    user_data = await state.get_data()
    group = user_data.get("group")
    subgroup = user_data.get("subgroup")
    assignments = await fetch_assignments_list(group=group, subgroup=subgroup)

    return render_assignments(assignments)
