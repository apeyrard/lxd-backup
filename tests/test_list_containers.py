from lxd_backup import list_containers

from fixtures import given_container


def test_no_container():
    assert [] == list_containers()


def test_one_container(given_container):
    given_container("test-container")
    assert ["test-container"] == list_containers()

def test_several_containers(given_container):
    given_container("test-container-1")
    given_container("test-container-2")
    assert "test-container-1" in list_containers()
    assert "test-container-2" in list_containers()
