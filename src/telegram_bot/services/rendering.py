from typing import Union, Optional

from ..models import Lesson, WeekDay, Teacher, ClassRoom
from ..utils import day_to_string, building_to_string


def render_week_schedule(lessons: list[Lesson]) -> str:
    week_schedule = []
    for day in WeekDay:
        one_day_lessons = [lesson for lesson in lessons if lesson.day == day]
        week_schedule.append(render_day_schedule(one_day_lessons, day))
    return "".join(week_schedule) or "Расписания не имеется"


def render_day_schedule(lessons: list[Lesson], day: Union[WeekDay, int]) -> str:
    if not lessons:
        return ""
    day = day_to_string(day)
    schedule = [f"\n\n----------------*{day.upper()}*----------------"] + \
               [render_lesson(lesson) for lesson in lessons]
    return '\n'.join(schedule)


def render_lesson(lesson: Lesson) -> str:
    teacher = render_teacher(lesson.teacher)
    classroom = render_classroom(lesson.classroom)
    return f"`{lesson.time}` - {lesson.subject.name}({lesson.kind}) - _{teacher}_. {classroom}"


def render_teacher(teacher: Teacher) -> str:
    return f"{teacher.second_name} {teacher.first_name} {teacher.middle_name}"


def render_classroom(classroom: Optional[ClassRoom]) -> str:
    if classroom is not None:
        building = building_to_string(classroom.building)
        number = classroom.number
        classroom_info = f"{building.upper()} ({number} аудитория)"
    else:
        classroom_info = ""
    return classroom_info
