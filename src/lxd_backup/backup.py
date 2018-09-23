#!/usr/bin/env python3

import os
import logging

from arrow import utcnow
from pylxd.exceptions import NotFound

from .containers import Container

logger = logging.getLogger(__name__)

def backup_container(name):
    try:
        container = Container(name)
    except NotFound:
        logger.warning(f'Cannot backup, container not found: {name}')
        return

    image = container.publish()
    image.add_alias('_'.join([today(), name]), '')


def today():
    return utcnow().format('YYYY-MM-DD')
