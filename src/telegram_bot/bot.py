from aiogram import Bot, types
from aiogram.contrib.fsm_storage.redis import RedisStorage
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.types import ParseMode, ReplyKeyboardRemove
from loguru import logger

from .keyboards import create_subgroup_list_keyboard, create_day_list_keyboard
from .models import Parity
from .models import Subgroup
from .services.api import fetch_lesson_list
from .services.api import get_week_schedule, get_groups_to_choose, get_day_schedule
from .services.date_time_utils import get_current_week_parity, get_next_week_parity
from .services.decorators import catch_error
from .services.redis_utils import get_available_groups
from .services.rendering import render_week_schedule, day_to_string_dict, string_to_day
from .settings import settings
from .states import ChooseGroup, ChooseDay

bot = Bot(token=settings.TELEGRAM_API_TOKEN)
dp = Dispatcher(
    bot,
    storage=RedisStorage(
        settings.redis_host,
        settings.redis_port,
        settings.redis_db,
    )
)


@logger.catch
async def startup(dispatcher: Dispatcher):
    logger.info("Бот успешно подключился к серверу")


@logger.catch
async def shutdown(dispatcher: Dispatcher):
    from .services.redis_utils import redis
    redis.close()
    logger.info("Соединение с Redis закрыто")
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()
    logger.info("Бот отключился от сервера")


@dp.message_handler(commands=['start'])
@catch_error
async def process_start_command(message: types.Message, state: FSMContext):
    greetings_message = "Привет, я бот, который помогает узнать расписание.\nВыбери свою группу"
    group_list_keyboard = await get_groups_to_choose()
    await ChooseGroup.waiting_for_group.set()
    await message.answer(greetings_message, reply_markup=group_list_keyboard)


@dp.message_handler(commands=['change_group'])
@catch_error
async def process_change_group_command(message: types.Message, state: FSMContext):
    group_list_keyboard = await get_groups_to_choose()
    await ChooseGroup.waiting_for_group.set()
    await message.answer("Выбери группу", reply_markup=group_list_keyboard)


@dp.message_handler(state=ChooseGroup.waiting_for_group)
@catch_error
async def group_chosen(message: types.Message, state: FSMContext):
    group_name = message.text
    available_groups = get_available_groups() or []

    if group_name not in available_groups:
        await message.answer("Такой группы нет в списке")
        return
    await state.update_data(group=group_name)
    await ChooseGroup.next()
    await message.answer("Группа успешно выбрана. Теперь выбери подгруппу. "
                         "Если твоя группа не делится на подгруппы, выбери вариант `'3'`",
                         reply_markup=create_subgroup_list_keyboard(), parse_mode=ParseMode.MARKDOWN)


@dp.message_handler(state=ChooseGroup.waiting_for_subgroup)
@catch_error
async def subgroup_chosen(message: types.Message, state: FSMContext):
    unsuccessful_choice_message = "Такой подгруппы нет"
    try:
        subgroup = int(message.text)
    except ValueError:
        await message.answer(unsuccessful_choice_message)
        return
    if subgroup not in [subgroup.value for subgroup in Subgroup]:
        await message.answer(unsuccessful_choice_message)
        return

    await state.update_data(subgroup=subgroup)
    await message.answer("Подгруппа успешно выбрана", reply_markup=ReplyKeyboardRemove())
    await state.reset_state(with_data=False)


@dp.message_handler(commands=['current_week'])
@catch_error
async def process_current_week_command(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    group = user_data["group"]
    response = await fetch_lesson_list(parity=1, group=group)
    reply_message = render_week_schedule(response)
    await message.answer(reply_message, parse_mode=ParseMode.MARKDOWN)


@dp.message_handler(commands=['numerator'])
@catch_error
async def process_numerator_command(message: types.Message, state: FSMContext):
    reply_message, reply_markup = await get_week_schedule(Parity.NUMERATOR, state)
    await message.answer(reply_message, parse_mode=ParseMode.MARKDOWN, reply_markup=reply_markup)


@dp.message_handler(commands=['denominator'])
@catch_error
async def process_denominator_command(message: types.Message, state: FSMContext):
    reply_message, reply_markup = await get_week_schedule(Parity.DENOMINATOR, state)
    await message.answer(reply_message, parse_mode=ParseMode.MARKDOWN, reply_markup=reply_markup)


@dp.message_handler(commands=['this_week'])
@catch_error
async def process_this_week_command(message: types.Message, state: FSMContext):
    parity = get_current_week_parity()
    reply_message, reply_markup = await get_week_schedule(parity, state)
    await message.answer(reply_message, parse_mode=ParseMode.MARKDOWN, reply_markup=reply_markup)


@dp.message_handler(commands=['next_week'])
@catch_error
async def process_next_week_command(message: types.Message, state: FSMContext):
    parity = get_next_week_parity()
    reply_message, reply_markup = await get_week_schedule(parity, state)
    await message.answer(reply_message, parse_mode=ParseMode.MARKDOWN, reply_markup=reply_markup)


@dp.message_handler(commands='day')
@catch_error
async def process_day_command(message: types.Message, state: FSMContext):
    await ChooseDay.waiting_for_day.set()
    await message.answer("Выбери день недели", reply_markup=create_day_list_keyboard())


@dp.message_handler(state=ChooseDay.waiting_for_day)
@catch_error
async def day_chosen(message: types.Message, state: FSMContext):
    day = message.text
    unsuccessful_choice_message = "Такого дня недели нет"

    if day not in day_to_string_dict.values():
        await message.answer(unsuccessful_choice_message)
        return

    parity = get_next_week_parity()
    day = string_to_day(day)
    schedule, keyboard = await get_day_schedule(parity, day, state)
    await message.answer(schedule, parse_mode=ParseMode.MARKDOWN, reply_markup=keyboard)
    await state.reset_state(with_data=False)
