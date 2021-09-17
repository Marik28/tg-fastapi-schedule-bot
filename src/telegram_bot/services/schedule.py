from aiogram.dispatcher import FSMContext

from telegram_bot.models import Parity
from telegram_bot.api.lessons import fetch_lesson_list
from telegram_bot.services.rendering import render_week_schedule, render_day_schedule


async def get_week_schedule(parity: Parity, state: FSMContext) -> str:
    """Получает расписание на неделю, используя переданную четность и состояние,
    из которого получает группу и подгруппу пользователя. Если у пользователя не выбрана группа или подгруппа,
    то состояние переключится на выбор оной"""
    user_data = await state.get_data()
    group = user_data.get("group")
    subgroup = user_data.get("subgroup")

    response = await fetch_lesson_list(parity=parity, group=group, subgroup=subgroup)
    return render_week_schedule(response)


async def get_day_schedule(
        parity: Parity,
        day: int,
        state: FSMContext
) -> str:
    user_data = await state.get_data()
    group = user_data.get("group")
    subgroup = user_data.get("subgroup")
    response = await fetch_lesson_list(parity=parity, group=group, subgroup=subgroup, day=day)
    schedule = render_day_schedule(response, day) or "В этот день пар нет"
    return schedule
