from .base import fetch
from ..models.assignments import Assignment
from ..settings import settings


async def fetch_assignments_list(
        group: str = None,
        subgroup: int = None,
        subject: str = None,
) -> list[Assignment]:
    query = {}
    if group is not None:
        query["group"] = group

    if subgroup is not None:
        query["subgroup"] = subgroup

    if subject is not None:
        query["subject"] = subject

    assignments = await fetch(settings.assignments_endpoint, query)

    return [Assignment.parse_obj(assignment) for assignment in assignments]
