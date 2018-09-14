import pytest

from pylxd import Client

@pytest.fixture
def given_container():

    client = Client()
    created_containers = []
    
    def create_container(name):
      container = client.containers.create({'name': name, 'source': {'type': 'none'}}, wait=True)
      created_containers.append(container)
      return
    
    yield create_container

    for container in created_containers:
        container.delete()
