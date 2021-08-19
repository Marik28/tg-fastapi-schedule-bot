from aiogram.dispatcher.filters.state import StatesGroup, State


class ChooseGroup(StatesGroup):
    """Состояние для выбора группы студентом. Сначала выбирается группа, затем подгруппа"""
    waiting_for_group = State()
    waiting_for_subgroup = State()


class ChooseDay(StatesGroup):
    """Состояние для выбора дня недели, на который необходимо узнать расписание"""
    waiting_for_day = State()
