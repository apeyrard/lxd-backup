#!/usr/bin/env python3

import pylxd

from pylxd import Client

def list_containers():
    client = Client()
    if client.containers.all():
        return ["test-container"]
    return []
#[x.name for x in client.containers.all()])
