from typing import Optional

from .base import fetch
from ..models import Subject
from ..settings import settings


async def fetch_subjects_list(group: Optional[str]) -> list[Subject]:
    query = {
        "with_links_only": str(True),
    }
    if group is not None:
        query["group"] = group
    subjects = await fetch(settings.subjects_endpoint, query)
    return [Subject.parse_obj(subject) for subject in subjects]
