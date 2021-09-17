from .base import fetch
from ..models import Group
from ..services.redis_utils import update_available_groups
from ..settings import settings


async def fetch_group_list() -> list[Group]:
    """Получает список доступных групп запросом с сервера"""
    group_list = await fetch(settings.groups_endpoint)
    groups: list[Group] = [Group.parse_obj(group) for group in group_list]
    update_available_groups([group.name for group in groups])
    return groups
