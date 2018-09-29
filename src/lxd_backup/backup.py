#!/usr/bin/env python3

import os
import logging
import shutil
import subprocess
import arrow

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
    
    execute_before_script(config)

    image = container.publish()

    execute_after_script(config)

    image_name = get_image_name(name, config)

    image.add_alias(image_name, '')

    if config and 'dir' in config:
        path = config['dir'].join(image_name)
        os.makedirs(config['dir'], exist_ok=True)
        in_file = image.export()
        with open(path, 'wb') as out_file:
            shutil.copyfileobj(in_file, out_file)
        image.delete()


def cleanup(config):
    for f in os.listdir(config['dir']):
        if 'until' in f:
            limit = f.split('_')[2]
            if arrow.get(limit).format('YYYY-MM-DD') < today():
                os.remove(config['dir'].join(f))

def execute_before_script(config):
    if config and 'before_script' in config:
        subprocess.call([config['before_script']])


def execute_after_script(config):
    if config and 'after_script' in config:
        subprocess.call([config['after_script']])


def get_image_name(name, config):
    if config and 'lifetime' in config:
        last_valid_date = get_date_from_lifetime(config['lifetime'])
        return '_'.join([today(), 'until', last_valid_date, name])
    return '_'.join([today(), name])
