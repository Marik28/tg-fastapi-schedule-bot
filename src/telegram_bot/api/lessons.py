from .base import fetch
from ..models import Lesson
from ..settings import settings


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
