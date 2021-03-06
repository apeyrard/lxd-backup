import pytest
import os

from pylxd import Client

from lxd_backup.storage.dir import Dir
from lxd_backup.storage.s3 import S3

@pytest.fixture
def client():
    return Client()

@pytest.fixture
def given_container(client, scope='session'):
    name = 'test-container'
    source = {'type': 'image',
              'mode': 'pull',
              'server': 'https://us.images.linuxcontainers.org',
              'protocol' : 'simplestreams',
              'alias': 'alpine/3.4/amd64'
              }
    container = client.containers.create({'name': name,
                                          'source': source},
                                          wait=True)
    yield name
    
    if container.status == 'Running':
        container.stop(wait=True)
    container.delete(wait=True)


@pytest.fixture
def given_running_container(client, given_container):
    container = client.containers.get(given_container)
    if container.status == 'Stopped':
        client.containers.get(given_container).start(wait=True)
    return given_container


@pytest.fixture
def given_stopped_container(client, given_container):
    container = client.containers.get(given_container)
    if container.status == 'Running':
        client.containers.get(given_container).stop(wait=True)
    return given_container


@pytest.fixture(params=[Dir, S3], scope='session')
def storage(request, tmpdir_factory):
    if request.param == Dir:
        instance = request.param(tmpdir_factory.mktemp('images'))
    elif request.param == S3:
        instance = request.param('apeyrard.com-test-bucket')

    yield instance
    instance.delete_all()
