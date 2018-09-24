from enum import Enum
from arrow import Arrow

def should_backup(frequency, target=None):
    if frequency == Frequency.DAILY:
        return True
    elif frequency == Frequency.WEEKLY:
        if target is None:
            target = 0
        return weekday() == target
    elif frequency == Frequency.MONTHLY:
        if target is None:
            target = 1
        return day() == target
    elif frequency == Frequency.BIANUALLY:
        if target is None:
            target = {'month': 1, 'day': 1}
        return month() % 6 == target['month'] and day() == target['day']

class Frequency(Enum):
    DAILY = 0
    WEEKLY = 1
    MONTHLY = 2
    BIANUALLY = 3


def day():
    return int(Arrow.utcnow().format('DD'))

def weekday():
    return Arrow.utcnow().weekday()

def month():
    return int(Arrow.utcnow().format('MM'))

