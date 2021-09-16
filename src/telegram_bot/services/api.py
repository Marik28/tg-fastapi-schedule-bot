from typing import Union

import aiohttp
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup

from ..keyboards import create_group_list_keyboard
from ..models import Group, Lesson, Parity
from ..models.assignments import Assignment
from ..services.redis_utils import update_available_groups
from ..services.rendering import render_week_schedule, render_day_schedule
from ..settings import settings


async def fetch(endpoint: str, query: dict = None) -> Union[dict, list]:
    """Корутина, делающая GET-запрос на переданный endpoint с переданными параметрами query.
    В случае успеха возвращает JSON ответ в виде объектов python."""
    async with aiohttp.ClientSession() as session:
        async with session.get(settings.api_base_url + endpoint, params=query) as response:
            if response.status == 200:
                response_json = await response.json()
                return response_json
            else:
                # todo исправить
                raise Exception("что то пошло не так")


async def fetch_group_list() -> list[Group]:
    """Получает список доступных групп запросом с сервера"""
    group_list = await fetch(settings.groups_endpoint)
    groups: list[Group] = [Group.parse_obj(group) for group in group_list]
    update_available_groups([group.name for group in groups])
    return groups


async def fetch_lesson_list(
        group: str = None,
        subgroup: int = None,
        parity: int = None,
        day: int = None
) -> list[Lesson]:
    """Получает список пар запросом с сервера"""
    query = {}

    # fixme что с этим сделать?

    if group is not None:
        query["group"] = group

    if subgroup is not None:
        query["subgroup"] = subgroup

    if parity is not None:
        query["parity"] = parity

    if day is not None:
        query["day"] = day
    lessons = await fetch(settings.lessons_endpoint, query)
    return [Lesson.parse_obj(lesson) for lesson in lessons]


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


async def get_groups_to_choose() -> ReplyKeyboardMarkup:
    """Ходит на эндпоинт со списком групп и возвращает клавиатуру с этим списком"""
    groups = await fetch_group_list()
    group_list_keyboard = create_group_list_keyboard(groups)
    return group_list_keyboard


async def fetch_assignments_list(
        group: str = None,
        subgroup: int = None,
        subject: str = None,
) -> list[Assignment]:
    query = {}
    if group is not None:
        query["group"] = group

    if subgroup is not None:
        query["subgroup"] = subgroup

    if subject is not None:
        query["subject"] = subject

    assignments = await fetch(settings.assignments_endpoint, query)

    return [Assignment.parse_obj(assignment) for assignment in assignments]
