from typing import Union, Optional

import aiohttp
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove

from ..keyboards import create_group_list_keyboard
from ..models import Group, Lesson, Parity
from ..services.redis_utils import update_available_groups
from ..services.rendering import render_week_schedule, render_day_schedule
from ..settings import settings
from ..states import ChooseGroup


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


async def get_week_schedule(parity: Parity, state: FSMContext) -> tuple[str, Optional[ReplyKeyboardMarkup]]:
    """Получает расписание на неделю, используя переданную четность и состояние,
    из которого получает группу и подгруппу пользователя. Если у пользователя не выбрана группа или подгруппа,
    то состояние переключится на выбор оной"""
    user_data = await state.get_data()
    group = user_data.get("group")
    subgroup = user_data.get("subgroup")
    if group is None or subgroup is None:
        group_list_keyboard = await get_groups_to_choose()
        await ChooseGroup.waiting_for_group.set()
        return "Необходимо выбрать группу и подгруппу", group_list_keyboard

    response = await fetch_lesson_list(parity=parity, group=group, subgroup=subgroup)
    return render_week_schedule(response), None


async def get_day_schedule(
        parity: Parity,
        day: int,
        state: FSMContext
) -> tuple[str, Union[ReplyKeyboardMarkup, ReplyKeyboardRemove]]:
    # todo избавиться от повторений
    user_data = await state.get_data()
    group = user_data.get("group")
    subgroup = user_data.get("subgroup")
    if group is None or subgroup is None:
        group_list_keyboard = await get_groups_to_choose()
        await ChooseGroup.waiting_for_group.set()
        return "Необходимо выбрать группу и подгруппу", group_list_keyboard
    response = await fetch_lesson_list(parity=parity, group=group, subgroup=subgroup, day=day)
    schedule = render_day_schedule(response, day) or "В этот день пар нет"
    return schedule, ReplyKeyboardRemove()


async def get_groups_to_choose() -> ReplyKeyboardMarkup:
    """Ходит на эндпоинт со списком групп и возвращает клавиатуру с этим списком"""
    groups = await fetch_group_list()
    group_list_keyboard = create_group_list_keyboard(groups)
    return group_list_keyboard


