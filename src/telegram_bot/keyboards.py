from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
)

from .models import Group, Subgroup
from .models import WeekDay
from .services.schedule import day_to_string


def create_group_list_keyboard(groups: list[Group]) -> ReplyKeyboardMarkup:
    """Создает список кнопок с названиями доступных групп"""
    group_list_buttons = [KeyboardButton(group.name) for group in groups]
    group_list_keyboard = ReplyKeyboardMarkup()
    for button in group_list_buttons:
        group_list_keyboard.add(button)
    return group_list_keyboard


def create_subgroup_list_keyboard() -> ReplyKeyboardMarkup:
    """Создает список кнопок с доступными подгруппами"""
    subgroup_list_buttons = [KeyboardButton(subgroup) for subgroup in Subgroup]
    subgroup_list_keyboard = ReplyKeyboardMarkup()
    for button in subgroup_list_buttons:
        subgroup_list_keyboard.add(button)
    return subgroup_list_keyboard


def create_day_list_keyboard() -> ReplyKeyboardMarkup:
    """Создает группу кнопок со списком дней недели"""
    day_list_buttons = [KeyboardButton(day_to_string(day)) for day in WeekDay]
    day_list_keyboard = ReplyKeyboardMarkup()
    for button in day_list_buttons:
        day_list_keyboard.add(button)
    return day_list_keyboard
