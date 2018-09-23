import pytest

from pylxd import Client

@pytest.fixture
def client():
    return Client()

@pytest.fixture
def given_container(client, scope='session'):
    name = 'test-container'
    source = {'type': 'image',
              'mode': 'pull',
              'server': 'https://cloud-images.ubuntu.com/daily',
              'protocol' : 'simplestreams',
              'alias': 'lts'
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
