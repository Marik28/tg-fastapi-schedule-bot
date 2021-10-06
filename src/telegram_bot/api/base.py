from typing import Union

import aiohttp
from aiohttp import ClientResponse
from loguru import logger

from ..exceptions import ServerError
from ..settings import settings


def is_server_side_error(response: ClientResponse) -> bool:
    status = response.status
    return 500 <= status <= 599


# todo много повторяющегося кода

async def fetch(endpoint: str, query: dict = None) -> Union[dict, list]:
    """Корутина, делающая GET-запрос на переданный endpoint с переданными параметрами query.
    В случае успеха возвращает JSON ответ в виде объектов python."""
    async with aiohttp.ClientSession() as session:
        async with session.get(settings.api_base_url + endpoint, params=query) as response:
            json_ = await response.json()
            if is_server_side_error(response):
                logger.error(json_)
                raise ServerError("Произошла непредвиденная ошибка на стороне сервера")
            return json_


async def post(endpoint: str, data: dict = None) -> ClientResponse:
    async with aiohttp.ClientSession() as session:
        async with session.post(settings.api_base_url + endpoint, json=data) as response:
            if is_server_side_error(response):
                json_ = await response.json()
                logger.error(json_)
                raise ServerError("Произошла непредвиденная ошибка на стороне сервера")
            elif response.status == 422:
                message = await response.json()
                logger.debug(message)
    return response


async def patch(endpoint: str, data: dict = None) -> ClientResponse:
    async with aiohttp.ClientSession() as session:
        async with session.patch(settings.api_base_url + endpoint, json=data) as response:
            if is_server_side_error(response):
                json_ = await response.json()
                logger.error(json_)
                raise ServerError("Произошла непредвиденная ошибка на стороне сервера")
    return response


async def put(endpoint: str, data: dict = None) -> ClientResponse:
    async with aiohttp.ClientSession() as session:
        async with session.put(settings.api_base_url + endpoint, json=data) as response:
            if is_server_side_error(response):
                json_ = await response.json()
                logger.error(json_)
                raise ServerError("Произошла непредвиденная ошибка на стороне сервера")
    return response
