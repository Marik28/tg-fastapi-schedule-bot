from aiogram.types import ReplyKeyboardMarkup

from ..api.groups import fetch_group_list
from ..keyboards import create_group_list_keyboard


async def get_groups_to_choose() -> ReplyKeyboardMarkup:
    """Ходит на эндпоинт со списком групп и возвращает клавиатуру с этим списком"""
    groups = await fetch_group_list()
    group_list_keyboard = create_group_list_keyboard(groups)
    return group_list_keyboard
