import traceback

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove
from aiogram.utils.exceptions import MessageIsTooLong
from aiohttp import ClientConnectorError
from loguru import logger

from ..exceptions import ServerError
from ..services.groups import get_groups_to_choose
from ..states import ChooseGroup

logger.add("../logs.log", level="INFO", rotation="2 MB", compression="zip")


def catch_error(func):
    """Декоратор для отлавливания ошибок. В случае возникновения ошибки уведомляет пользователя и пишет лог"""

    async def wrapper(message: types.Message, state: FSMContext, *args, **kwargs):
        logger.debug(f"{message.text}, {message.from_user}")
        msg = None
        try:
            await func(message, state)
        except ClientConnectorError:
            msg = "Сервер не отвечает"

            logger.error(f"Message: {message.text}, user: {message.from_user}, error: {traceback.format_exc()}")
        except ServerError:
            msg = "Произошла ошибка на стороне сервера"
            logger.error(f"Message: {message.text}, user: {message.from_user}, error: {traceback.format_exc()}")

        except MessageIsTooLong:
            msg = "Сформированное сообщение слишком длинное. Хз, что делать 🤔"
            logger.error(f"Message: {message.text}, user: {message.from_user}, error: {traceback.format_exc()}")

        except Exception:
            msg = "Произошла непредвиденная ошибка"
            logger.error(f"Message: {message.text}, user: {message.from_user}, error: {traceback.format_exc()}")
        finally:
            if msg is not None:
                await message.answer(msg, reply_markup=ReplyKeyboardRemove())
                await state.reset_state(with_data=False)

    return wrapper


def group_chosen_required(func):
    """
    Декоратор, для команды бота, проверяет наличие данных в хранилище о группе и подгруппе
    пользователя перед вызовом хендлера команды. Если данных нет, предлагает пользователю выбрать их.
    """

    async def wrapper(message: types.Message, state: FSMContext, *args, **kwargs):
        user_data = await state.get_data()
        group = user_data.get("group")
        subgroup = user_data.get("subgroup")
        if group is None or subgroup is None:
            group_list_keyboard = await get_groups_to_choose()
            await ChooseGroup.waiting_for_group.set()
            await message.answer("Необходимо выбрать группу и подгруппу", reply_markup=group_list_keyboard)
        else:
            await func(message, state)

    return wrapper
