#!/usr/bin/env python3

import pylxd
import os
import logging

from pylxd import Client

logging.basicConfig(filename='lxd-backup.log', format='%(asctime)s - %(levelname)s: %(message)s', level=logging.INFO)

def publish_container(name):
    client = Client()

    try:
        container = client.containers.get(name)
        container.stop(wait=True)
        image = container.publish(wait=True)
        image.add_alias('_'.join(['2018-09-22', name]), '')
        container.start(wait=True)
    except pylxd.exceptions.NotFound:
        logging.warning(f'Cannot publish, container not found: {name}')
    except pylxd.exceptions.LXDAPIException:
        logging.warning(f'Cannot publish, container not stopped: {name}')
        container.start(wait=True)

