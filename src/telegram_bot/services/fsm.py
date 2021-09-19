from aiogram.dispatcher import FSMContext


async def get_group_and_subgroup(state: FSMContext) -> tuple[str, int]:
    """

    :param state: FSM
    :return: (group, subgroup)
    """
    user_data = await state.get_data()
    group = user_data.get("group")
    subgroup = user_data.get("subgroup")
    return group, subgroup
