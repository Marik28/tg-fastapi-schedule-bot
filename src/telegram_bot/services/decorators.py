import traceback

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove
from aiohttp import ClientConnectorError
from loguru import logger

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
        except Exception:
            msg = "Произошла непредвиденная ошибка"
            logger.error(f"Message: {message.text}, user: {message.from_user}, error: {traceback.format_exc()}")
        finally:
            if msg is not None:
                await message.answer(msg, reply_markup=ReplyKeyboardRemove())
                await state.reset_state(with_data=False)

    return wrapper
