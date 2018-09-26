#!/usr/bin/env python3

import os
import logging
import shutil

from pylxd.exceptions import NotFound

from .containers import Container
from .time import (today, get_date_from_lifetime)

logger = logging.getLogger(__name__)


def backup_container(name, config=None):
    try:
        container = Container(name)
    except NotFound:
        logger.warning(f'Cannot backup, container not found: {name}')
        return

    image = container.publish()

    if config and 'lifetime' in config:
        last_valid_date = get_date_from_lifetime(config['lifetime'])
        image_name = '_'.join([today(), 'until', last_valid_date, name])
    else:
        image_name = '_'.join([today(), name])

    image.add_alias(image_name, '')

    if config and 'dir' in config:
        path = config['dir'].join(image_name)
        os.makedirs(config['dir'], exist_ok=True)
        in_file = image.export()
        with open(path, 'wb') as out_file:
            shutil.copyfileobj(in_file, out_file)
        image.delete()
