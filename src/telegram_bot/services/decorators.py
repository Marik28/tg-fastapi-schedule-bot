import traceback

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiohttp import ClientConnectorError
from loguru import logger

logger.add("../logs.log", level="INFO", rotation="2 MB", compression="zip")


def catch_error(func):
    """Декоратор для отлавливания ошибок. В случае возникновения ошибки уведомляет пользователя и пишет лог"""

    async def wrapper(message: types.Message, state: FSMContext, *args, **kwargs):
        logger.debug(f"{message.text}, {message.from_user}")
        try:
            await func(message, state)
        except ClientConnectorError:
            msg = "Сервер не отвечает"
            await message.answer(msg)
            logger.error(f"Message: {message.text}, user: {message.from_user}, error: {traceback.format_exc()}")
            raise
        except Exception:
            msg = "Произошла непредвиденная ошибка"
            await message.answer(msg)
            logger.error(f"Message: {message.text}, user: {message.from_user}, error: {traceback.format_exc()}")
            raise

    return wrapper
