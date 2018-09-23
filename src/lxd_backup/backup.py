#!/usr/bin/env python3

import os
import logging
import shutil
from arrow import Arrow

from pylxd.exceptions import NotFound

from .containers import Container
from .frequencies import Frequency

logger = logging.getLogger(__name__)

def backup_container(name, config=None):
    try:
        container = Container(name)
    except NotFound:
        logger.warning(f'Cannot backup, container not found: {name}')
        return

    image = container.publish()
    image_name = '_'.join([today(), name])
    image.add_alias(image_name, '')

    if config:
        path = config['dir'].join(image_name)
        os.makedirs(config['dir'], exist_ok=True)
        in_file = image.export()
        with open(path, 'wb') as out_file:
            shutil.copyfileobj(in_file, out_file)
        image.delete()

def month_and_day():
    return Arrow.utcnow().format('MM-DD')

def today():
    return Arrow.utcnow().format('YYYY-MM-DD')

def day():
    return int(Arrow.utcnow().format('DD'))

def weekday():
    return Arrow.utcnow().weekday()

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
        return True

