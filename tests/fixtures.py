import pytest

from pylxd import Client

@pytest.fixture
def client():
    return Client()

@pytest.fixture
def given_container():
    client = Client()

    created_containers = []
    
    def create_container(name):
        source = {'type': 'image',
                  'mode': 'pull',
                  'server': 'https://cloud-images.ubuntu.com/daily',
                  'protocol' : 'simplestreams',
                  'alias': 'lts'
                  }
        container = client.containers.create({'name': name,
                                              'source': source},
                                              wait=True)
        container.start(wait=True)
        created_containers.append(container)
        return
    
    yield create_container

    for container in created_containers:
        container.stop(wait=True)
        container.delete(wait=True)
