import pytest
from arrow import utcnow

from lxd_backup.backup import backup_container
from lxd_backup.storage.dir import Dir
from lxd_backup.storage.s3 import S3
from fixtures import given_container, given_stopped_container, client, storage

def test_export_one_container_then_image_deleted(given_stopped_container, client, storage):
    container_name = given_stopped_container
    image = backup_container(container_name)
    
    storage.export(image)

    unexpected_file = '_'.join([utcnow().format('YYYY-MM-DD'), container_name])
    assert not client.images.exists(unexpected_file, alias=True)


def test_export_one_container_then_file_exists(given_stopped_container, storage):
    container_name = given_stopped_container
    image = backup_container(container_name)

    storage.export(image)

    expected_file = '_'.join([utcnow().format('YYYY-MM-DD'), container_name])
    assert storage.exists(expected_file)


def test_when_obsolete_backup_then_delete_it(mocker, storage):
    storage.create_file('1992-10-26_until_1998-01-15_test-container')

    storage.cleanup()

    assert not storage.exists('1992-10-26_until_1998-01-15_test-container')


def test_when_not_obsolete_backup_then_dont_delete_it(mocker, storage):
    mocker.patch('lxd_backup.storage.today', return_value='1995-12-25')

    filename = '1992-10-26_until_1998-01-15_test-container'
    storage.create_file(filename)

    storage.cleanup()

    assert storage.exists(filename)


def test_when_obsolete_day_is_today_then_dont_delete_it(mocker, storage):
    mocker.patch('lxd_backup.storage.today', return_value='1995-12-25')

    filename = '1992-10-26_until_1995-12-25_test-container'
    storage.create_file(filename)

    storage.cleanup()

    assert storage.exists(filename)


def test_when_export_image_then_export_hash(mocker, storage, given_stopped_container):
    container_name = given_stopped_container
    image = backup_container(container_name)

    storage.export(image)

    expected_file = '_'.join([utcnow().format('YYYY-MM-DD'), container_name])
    expected_hash_file = ''.join([expected_file, '.md5'])
    assert storage.exists(expected_file)
    assert storage.exists(expected_hash_file)

