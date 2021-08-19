from typing import Optional, Iterable

from redis import Redis

from ..settings import settings

redis = Redis(
    settings.redis_host,
    settings.redis_port,
    settings.redis_db,
    decode_responses=True
)


def get_available_groups() -> Optional[set[str]]:
    """Возвращает множество групп, для которых доступно отслеживание расписания"""
    return redis.smembers(settings.available_groups_set_name)


def update_available_groups(groups_names: Iterable[str]) -> None:
    """Обновляет множество групп, для которых доступно отслеживание расписания"""
    redis.delete(settings.available_groups_set_name)
    redis.sadd(settings.available_groups_set_name, *groups_names)
