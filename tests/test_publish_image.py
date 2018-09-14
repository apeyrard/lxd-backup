from lxd_backup import list_containers
from lxd_backup import publish_container

from fixtures import given_container

def test_unkown_container():
    result = publish_container("unknown")
    assert result == False

def test_publish_one_container(given_container):
    given_container("a-container")

    result = publish_container("a-container")
    assert result == True
