import datetime as dt

import pytz

from telegram_bot.models import Parity
from telegram_bot.settings import settings

timezone = pytz.timezone(settings.timezone_id)


def now() -> dt.datetime:
    """Возвращает текущие дату и время в часовом поясе, заданном в настройках"""
    utc = pytz.utc
    utc_now: dt.datetime = utc.localize(dt.datetime.utcnow())
    return utc_now.astimezone(timezone)


def get_week_day(datetime: dt.datetime) -> int:
    """Возвращает номер дня недели"""
    day_number = int(datetime.strftime("%w"))
    return 7 if day_number == 0 else day_number


def get_today() -> int:
    """Возвращает номер сегодняшнего дня недели"""
    return get_week_day(now())


def get_tomorrow() -> int:
    """Возвращает номер завтрашнего дня недели"""
    return get_week_day(now() + dt.timedelta(days=1))


def parse_parity(week_num: int) -> Parity:
    """Получает четность, исходя из порядкового номера недели"""
    return Parity.NUMERATOR if (settings.start_week - week_num) % 2 == 0 else Parity.DENOMINATOR


def get_week_parity(datetime: dt.datetime) -> Parity:
    """Возвращает четность недели в виде перечисления Parity"""
    return parse_parity(int(datetime.strftime('%W')))


def get_current_week_parity() -> Parity:
    """Возвращает четность текущей недели в виде перечисления Parity"""
    return get_week_parity(now())


def get_next_week_parity() -> Parity:
    """Возвращает четность следующей недели в виде перечисления Parity"""
    return get_week_parity(now() + dt.timedelta(weeks=1))
