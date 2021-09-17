from .base import fetch
from ..models import Subject
from ..settings import settings


async def fetch_subjects_list() -> list[Subject]:
    query = {
        "with_links_only": str(True),
    }
    subjects = await fetch(settings.subjects_endpoint, query)
    return [Subject.parse_obj(subject) for subject in subjects]
