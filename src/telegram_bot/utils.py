from .models import Building, WeekDay

building_to_string_dict = {
    Building.MAIN: "главный корпус",
    Building.FIRST: "корпус №1",
    Building.SECOND: "корпус №2",
    Building.THIRD: "корпус №3",
    Building.FOURTH: "корпус №4",
}
day_to_string_dict: dict[int, str] = {
    WeekDay.MONDAY: "понедельник",
    WeekDay.TUESDAY: "вторник",
    WeekDay.WEDNESDAY: "среда",
    WeekDay.THURSDAY: "четверг",
    WeekDay.FRIDAY: "пятница",
    WeekDay.SATURDAY: "суббота",
    WeekDay.SUNDAY: "воскресенье",
}
string_to_day_dict = {
    value: key for key, value in day_to_string_dict.items()
}


def string_to_day(day_name: str) -> int:
    """Принимает название дня недели в виде строки, возвращает его порядковый номер"""
    return string_to_day_dict[day_name]


def day_to_string(day: int) -> str:
    return day_to_string_dict[day]


def building_to_string(building: Building) -> str:
    return building_to_string_dict[building]
