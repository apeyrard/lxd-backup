#!/usr/bin/env python3

import pylxd

from pylxd import Client

client = Client()

def list_containers():
    return []
#[x.name for x in client.containers.all()])
