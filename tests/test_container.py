from lxd_backup.backup import backup_container
from fixtures import given_container, given_running_container, given_stopped_container, client

from lxd_backup.containers import Container

def test_when_start_already_running_container(given_running_container, client):
    container_name = given_running_container

    container = Container(container_name)
    container.start()

    assert client.containers.get(container_name).status == 'Running'

def test_when_stop_already_stopped_container(given_stopped_container, client):
    container_name = given_stopped_container

    container = Container(container_name)
    container.stop()

    assert client.containers.get(container_name).status == 'Stopped'
