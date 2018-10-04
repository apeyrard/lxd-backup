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
    return default_target[frequency]


def should_backup(frequency, target=None):
    if target is None:
        try:
            target = get_default_target(frequency)
        except KeyError:
            return False

    if frequency == Frequency.DAILY:
        return True
    elif frequency == Frequency.WEEKLY:
        return weekday() == target
    elif frequency == Frequency.MONTHLY:
        return day() == target
    elif frequency == Frequency.BIANUALLY:
        return month() % 6 == target['month'] and day() == target['day']
    else:
        return False
