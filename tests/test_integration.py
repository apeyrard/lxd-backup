import os
import pytest
import io
from arrow import Arrow

from lxd_backup.cli import parse_config
from fixtures import given_container, given_stopped_container, client, storage


def test_when_use_config_file_to_export(mocker, given_stopped_container):
    container_name = given_stopped_container

    
    parse_config('tests/test_files/dir/nominal.json')


    expected_file = '_'.join([Arrow.utcnow().format('YYYY-MM-DD'), 'until', Arrow.utcnow().format('YYYY-MM-DD'), container_name])
    expected_hash_file = ''.join([expected_file, '.md5'])

    with open('tmp/before_script_was_run') as f:
        before_script_result = f.readline() == 'True\n'
    with open('tmp/after_script_was_run') as f:
        after_script_result = f.readline() == 'True\n'
    
    assert os.path.isfile(os.path.join('/tmp/images', expected_file))
    assert os.path.isfile(os.path.join('/tmp/images', expected_hash_file))
    assert before_script_result
    assert after_script_result

