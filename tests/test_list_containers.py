import pytest
from pylxd import Client

from lxd_backup import list_containers

@pytest.fixture
def container(name):
    client = Client()
    yield client.containers.create({'name': name, 'source': {'type': 'none'}}, wait=True)
    client.containers.get(name).delete()

def test_no_container():
    assert [] == list_containers()

def test_one_container():
    assert ["test-container"] == list_containers()
