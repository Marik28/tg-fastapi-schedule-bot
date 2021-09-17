from typing import Union

import aiohttp

from telegram_bot.settings import settings


async def fetch(endpoint: str, query: dict = None) -> Union[dict, list]:
    """Корутина, делающая GET-запрос на переданный endpoint с переданными параметрами query.
    В случае успеха возвращает JSON ответ в виде объектов python."""
    async with aiohttp.ClientSession() as session:
        async with session.get(settings.api_base_url + endpoint, params=query) as response:
            if response.status == 200:
                response_json = await response.json()
                return response_json
            else:
                # todo исправить
                raise Exception("что то пошло не так")