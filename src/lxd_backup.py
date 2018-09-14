#!/usr/bin/env python3

import pylxd

from pylxd import Client

def list_containers():
    client = Client()
    return [x.name for x in client.containers.all()]

def publish_container(name):
    return False
