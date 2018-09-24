import os

from arrow import utcnow

from lxd_backup.backup import backup_container
from fixtures import given_container, given_running_container, given_stopped_container, client

def test_when_unknown_container_then_nothing(client):
    container_name = 'unknown'
    date = utcnow().format('YYYY-MM-DD')
    backup_container(container_name)

    assert not client.images.exists('_'.join([date, container_name]), alias=True)

def test_when_nominal_then_container_is_running_after_backup(given_running_container, client):
    container_name = given_running_container
    date = utcnow().format('YYYY-MM-DD')

    backup_container(container_name)
    client.images.get_by_alias('_'.join([date, container_name])).delete()
    assert client.containers.get(container_name).status == 'Running'

def test_when_container_stopped_then_container_stopped_after_backup(given_stopped_container, client):
    container_name = given_stopped_container
    date = utcnow().format('YYYY-MM-DD')

    backup_container(container_name)
   
    client.images.get_by_alias('_'.join([date, container_name])).delete()
    assert client.containers.get(container_name).status == 'Stopped'

def test_when_nominal_then_image_exists(given_stopped_container, client):
    container_name = given_stopped_container
    date = utcnow().format('YYYY-MM-DD')

    backup_container(container_name)
    result = client.images.exists('_'.join([date, container_name]), alias=True)

    client.images.get_by_alias('_'.join([date, container_name])).delete()

    assert result


def test_when_nominal_then_image_alias_contains_date(given_stopped_container, client, mocker):
    container_name = given_stopped_container
    date = '1999-08-12'
    mocker.patch('lxd_backup.backup.today', return_value=date)

    backup_container(container_name)
   
    result = client.images.exists('_'.join([date, container_name]), alias=True)

    client.images.get_by_alias('_'.join([date, container_name])).delete()
    assert result
