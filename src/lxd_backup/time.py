from arrow import Arrow
from collections import defaultdict


def today():
    return Arrow.utcnow().format('YYYY-MM-DD')


def day():
    return int(Arrow.utcnow().format('DD'))


def weekday():
    return Arrow.utcnow().weekday()


def month():
    return int(Arrow.utcnow().format('MM'))


def get_date_from_lifetime(lifetime):
    lifetime = defaultdict(lambda: 0, lifetime)
    return Arrow.utcnow().shift(days=lifetime['days'],
                                weeks=lifetime['weeks'],
                                months=lifetime['months'],
                                years=lifetime['years']).format('YYYY-MM-DD')
