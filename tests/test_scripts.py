import shutil

from lxd_backup.backup import backup_container
from fixtures import given_container, given_running_container, given_stopped_container, client

def test_when_given_before_script_then_script_is_run(given_stopped_container, mocker, client):
    date = '2017-12-14'
    mocker.patch('lxd_backup.backup.today', return_value=date)
    container_name = given_stopped_container
    expected_image = '_'.join([date, container_name])
    config = {'before_script': './tests/test_before_script.sh'} 

    backup_container(container_name, config)

    client.images.get_by_alias(expected_image).delete()

    with open('tmp/before_script_was_run') as f:
        result = f.readline() == 'True\n'

    shutil.rmtree('tmp')

    assert result

def test_when_given_after_script_then_script_is_run(given_stopped_container, mocker, client):
    date = '2017-12-14'
    mocker.patch('lxd_backup.backup.today', return_value=date)
    container_name = given_stopped_container
    expected_image = '_'.join([date, container_name])
    config = {'after_script': './tests/test_after_script.sh'} 

    backup_container(container_name, config)

    client.images.get_by_alias(expected_image).delete()

    with open('tmp/after_script_was_run') as f:
        result = f.readline() == 'True\n'

    shutil.rmtree('tmp')

    assert result
