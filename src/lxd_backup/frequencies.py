from enum import Enum
from .time import (weekday,
                   day,
                   month)


class Frequency(Enum):
    DAILY = 0
    WEEKLY = 1
    MONTHLY = 2
    BIANUALLY = 3


def get_default_target(frequency):
    default_target = {
        Frequency.DAILY: None,
        Frequency.WEEKLY: 0,
        Frequency.MONTHLY: 1,
        Frequency.BIANUALLY: {'month': 1, 'day': 1}
    }
    return default_target.get(frequency)


def should_backup(frequency, target=None):
    result = False

    if target is None:
        target = get_default_target(frequency)

    if frequency == Frequency.DAILY:
        result = True
    elif frequency == Frequency.WEEKLY:
        result = weekday() == target
    elif frequency == Frequency.MONTHLY:
        result = day() == target
    elif frequency == Frequency.BIANUALLY:
        result = is_day_biannual_target(target)

    return result


def is_day_biannual_target(target):
    return month() % 6 == target['month'] % 6 and day() == target['day']
