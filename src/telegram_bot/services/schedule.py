from typing import Union, Optional

from aiogram.dispatcher import FSMContext

from .fsm import get_group_and_subgroup
from ..api.lessons import fetch_lesson_list
from ..models import Parity, Lesson, WeekDay, Teacher, ClassRoom, Building


async def get_week_schedule(parity: Parity, state: FSMContext) -> str:
    """Получает расписание на неделю, используя переданную четность и состояние,
    из которого получает группу и подгруппу пользователя. Если у пользователя не выбрана группа или подгруппа,
    то состояние переключится на выбор оной"""
    group, subgroup = await get_group_and_subgroup(state)
    response = await fetch_lesson_list(parity=parity, group=group, subgroup=subgroup)
    return render_week_schedule(response)


async def get_day_schedule(
        parity: Parity,
        day: int,
        state: FSMContext
) -> str:
    group, subgroup = await get_group_and_subgroup(state)
    response = await fetch_lesson_list(parity=parity, group=group, subgroup=subgroup, day=day)
    schedule = render_day_schedule(response, day) or "В этот день пар нет"
    return schedule


def render_week_schedule(lessons: list[Lesson]) -> str:
    """Формирует строку с расписанием на неделю"""
    week_schedule = []
    for day in WeekDay:
        one_day_lessons = [lesson for lesson in lessons if lesson.day == day]
        week_schedule.append(render_day_schedule(one_day_lessons, day))
    return "".join(week_schedule) or "Расписания не имеется"


def render_day_schedule(lessons: list[Lesson], day: Union[WeekDay, int]) -> str:
    """Формирует строку с расписанием на день"""
    if not lessons:
        return ""
    day = day_to_string(day)
    schedule = [f"\n\n`{day.upper():-^30}`"] + \
               [render_lesson(lesson) for lesson in lessons]
    return '\n'.join(schedule)


def render_lesson(lesson: Lesson) -> str:
    """Формирует строку с информацией о паре"""
    teacher = render_teacher(lesson.teacher)
    classroom = render_classroom(lesson.classroom)
    return f"`{lesson.time}` - {lesson.subject.name}({lesson.kind}) - _{teacher}_. {classroom}"


def render_teacher(teacher: Teacher) -> str:
    """Формирует строку с информацией о преподавателе"""
    return f"{teacher.second_name} {teacher.first_name} {teacher.middle_name}"


def render_classroom(classroom: Optional[ClassRoom]) -> str:
    """Формирует строку с информацией о аудитории"""
    if classroom is not None:
        building = building_to_string(classroom.building)
        number = classroom.number
        classroom_info = f"{building.upper()} ({number} аудитория)"
    else:
        classroom_info = ""
    return classroom_info


building_to_string_dict = {
    Building.MAIN: "главный корпус",
    Building.FIRST: "корпус №1",
    Building.SECOND: "корпус №2",
    Building.THIRD: "корпус №3",
    Building.FOURTH: "корпус №4",
}
day_to_string_dict: dict[int, str] = {
    WeekDay.MONDAY: "понедельник",
    WeekDay.TUESDAY: "вторник",
    WeekDay.WEDNESDAY: "среда",
    WeekDay.THURSDAY: "четверг",
    WeekDay.FRIDAY: "пятница",
    WeekDay.SATURDAY: "суббота",
    WeekDay.SUNDAY: "воскресенье",
}
string_to_day_dict = {
    value: key for key, value in day_to_string_dict.items()
}


def string_to_day(day_name: str) -> int:
    """Принимает название дня недели в виде строки, возвращает его порядковый номер (1-7)"""
    return string_to_day_dict[day_name]


def day_to_string(day: int) -> str:
    """Принимает порядковый номер дня недели (1-7), возвращает название дня недели в виде строки"""
    return day_to_string_dict[day]


def building_to_string(building: Building) -> str:
    """Возвращает строку с названием корпуса"""
    return building_to_string_dict[building]
