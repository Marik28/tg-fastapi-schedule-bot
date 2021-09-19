from aiogram.dispatcher import FSMContext
from aiogram.utils.markdown import hbold

from .fsm import get_group_and_subgroup
from ..api.subjects import fetch_subjects_list
from ..models import Subject, UsefulLink


def render_useful_links(links: list[UsefulLink]) -> str:
    msg_bits = []
    for index, link in enumerate(links, start=1):
        url = link.link
        description = link.description
        msg_bits.append(f"{index}. 🔗 {url}")
        if description:
            msg_bits.append(f"Описание - {description}")
    return '\n'.join(msg_bits)


def render_subjects(subjects: list[Subject]) -> str:
    if not subjects:
        return "Полезных ссылок нет"

    msg_bits = []
    for subject in subjects:
        subject_name = subject.name
        links_info = render_useful_links(subject.useful_links)
        msg_bits.append(f"📝 {hbold('Предмет')} - {subject_name}")
        msg_bits.append(links_info)
        msg_bits.append("-------------------")

    return '\n'.join(msg_bits)


async def get_subjects(state: FSMContext) -> str:
    group, _ = await get_group_and_subgroup(state)
    subjects = await fetch_subjects_list(group=group)
    return render_subjects(subjects)
