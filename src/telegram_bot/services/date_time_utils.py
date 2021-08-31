import datetime as dt

from telegram_bot.models import Parity
from telegram_bot.settings import settings


def parse_parity(week_num: int) -> Parity:
    """Получает четность, исходя из порядкового номера недели"""
    return Parity.NUMERATOR if (settings.start_week - week_num) % 2 == 0 else Parity.DENOMINATOR


def get_current_week_parity() -> Parity:
    """Возвращает четность недели в виде строки Parity"""
    cur_week = int(dt.date.today().strftime('%W'))
    return parse_parity(cur_week)


def get_next_week_parity() -> Parity:
    """Возвращает четность недели в виде перечисления Parity"""
    next_week = int(dt.date.today().strftime('%W')) + 1
    return parse_parity(next_week)
