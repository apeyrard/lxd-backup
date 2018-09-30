#!/usr/bin/env python3

import logging
import subprocess

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

    return image




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
