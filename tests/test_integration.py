import os
import pytest
import io
from arrow import Arrow

from lxd_backup.cli import parse_config
from lxd_backup.storage.dir import Dir
from lxd_backup.storage.s3 import S3
from fixtures import given_container, given_stopped_container, client, storage


def test_when_use_config_file_to_export(mocker, given_stopped_container):
    container_name = given_stopped_container

    
    parse_config('tests/test_files/dir/nominal.json')


    expected_file = '_'.join([Arrow.utcnow().format('YYYY-MM-DD'), 'until', Arrow.utcnow().shift(days=1).format('YYYY-MM-DD'), container_name])
    expected_hash_file = ''.join([expected_file, '.md5'])

    with open('tmp/before_script_was_run') as f:
        before_script_result = f.readline() == 'True\n'
    with open('tmp/after_script_was_run') as f:
        after_script_result = f.readline() == 'True\n'

    file_exists = os.path.isfile(os.path.join('/tmp/images', expected_file))
    hash_exists = os.path.isfile(os.path.join('/tmp/images', expected_hash_file))
    
    Dir('/tmp/images').delete_all()

    assert file_exists
    assert hash_exists
    assert before_script_result
    assert after_script_result


def test_when_several_backups_only_backup_longest_lifetime(mocker, given_stopped_container):
    mocker.patch('lxd_backup.cli.should_backup', return_value=True)
    container_name = given_stopped_container
    s3 = S3('apeyrard.com-test-bucket')

    expected_file = '_'.join([Arrow.utcnow().format('YYYY-MM-DD'), 'until', Arrow.utcnow().shift(months=1).format('YYYY-MM-DD'), container_name])
    expected_hash_file = ''.join([expected_file, '.md5'])
    unexpected_file = '_'.join([Arrow.utcnow().format('YYYY-MM-DD'), 'until', Arrow.utcnow().shift(days=1).format('YYYY-MM-DD'), container_name])

    parse_config('tests/test_files/s3/several_backups_same_day.json')

    with open('tmp/before_script_was_run') as f:
        before_script_result = f.readline() == 'True\n'
    with open('tmp/after_script_was_run') as f:
        after_script_result = f.readline() == 'True\n'

    file_exists = s3.exists(expected_file)
    hash_exists = s3.exists(expected_hash_file)
    file_does_not_exist = not s3.exists(unexpected_file)

    s3.delete_all()

    assert file_exists
    assert hash_exists
    assert before_script_result
    assert after_script_result
    assert file_does_not_exist


def test_when_several_backups_only_backup_longest_lifetime_oldest_is_deactivated(mocker, given_stopped_container):
    container_name = given_stopped_container
    s3 = S3('apeyrard.com-test-bucket')

    unexpected_file = '_'.join([Arrow.utcnow().format('YYYY-MM-DD'), 'until', Arrow.utcnow().shift(months=1).format('YYYY-MM-DD'), container_name])
    expected_file = '_'.join([Arrow.utcnow().format('YYYY-MM-DD'), 'until', Arrow.utcnow().shift(days=1).format('YYYY-MM-DD'), container_name])

    parse_config('tests/test_files/s3/several_backups_same_day_oldest_is_deactivated.json')

    with open('tmp/before_script_was_run') as f:
        before_script_result = f.readline() == 'True\n'
    with open('tmp/after_script_was_run') as f:
        after_script_result = f.readline() == 'True\n'

    file_exists = s3.exists(expected_file)
    file_does_not_exist = not s3.exists(unexpected_file)

    s3.delete_all()

    assert file_exists
    assert before_script_result
    assert after_script_result
    assert file_does_not_exist


def test_when_several_backups_only_backup_longest_lifetime_oldest_is_daily(mocker, given_stopped_container):
    mocker.patch('lxd_backup.cli.should_backup', return_value=True)
    container_name = given_stopped_container
    s3 = S3('apeyrard.com-test-bucket')

    unexpected_file = '_'.join([Arrow.utcnow().format('YYYY-MM-DD'), 'until', Arrow.utcnow().shift(months=1).format('YYYY-MM-DD'), container_name])
    expected_file = '_'.join([Arrow.utcnow().format('YYYY-MM-DD'), 'until', Arrow.utcnow().shift(days=365).format('YYYY-MM-DD'), container_name])

    parse_config('tests/test_files/s3/several_backups_same_day_oldest_is_daily.json')

    with open('tmp/before_script_was_run') as f:
        before_script_result = f.readline() == 'True\n'
    with open('tmp/after_script_was_run') as f:
        after_script_result = f.readline() == 'True\n'

    file_exists = s3.exists(expected_file)
    file_does_not_exist = not s3.exists(unexpected_file)

    s3.delete_all()

    assert file_exists
    assert before_script_result
    assert after_script_result
    assert file_does_not_exist
