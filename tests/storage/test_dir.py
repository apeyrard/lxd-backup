import os
from arrow import utcnow

from lxd_backup.backup import backup_container, cleanup
from fixtures import given_container, given_stopped_container, client


def test_export_one_container_then_image_deleted(given_stopped_container, tmpdir, client):
    container_name = given_stopped_container
    export_dir = tmpdir.join('images')

    config = {'dir': export_dir}
    backup_container(container_name, config=config)

    expected_file = '_'.join([utcnow().format('YYYY-MM-DD'), container_name])
    assert not client.images.exists(expected_file, alias=True)

def test_export_one_container_then_file_exists(given_stopped_container, tmpdir):
    container_name = given_stopped_container
    export_dir = tmpdir.join('images')

    config = {'dir': export_dir}
    backup_container(container_name, config=config)

    expected_file = '_'.join([utcnow().format('YYYY-MM-DD'), container_name])
    assert os.path.isfile(export_dir.join(expected_file))
    
def test_when_obsolete_backup_then_delete_it(mocker, tmpdir):
    export_dir = tmpdir.join('images')
    os.makedirs(export_dir, exist_ok=True)
    config = {'dir': export_dir}

    filename = '1992-10-26_until_1998-01-15_test-container'
    open(export_dir.join(filename), 'w+').close() 

    cleanup(config)

    assert not os.path.isfile(export_dir.join(filename))


def test_when_not_obsolete_backup_then_dont_delete_it(mocker, tmpdir):
    mocker.patch('lxd_backup.backup.today', return_value='1995-12-25')
    export_dir = tmpdir.join('images')
    os.makedirs(export_dir, exist_ok=True)
    config = {'dir': export_dir}

    filename = '1992-10-26_until_1998-01-15_test-container'
    open(export_dir.join(filename), 'w+').close() 

    cleanup(config)

    assert os.path.isfile(export_dir.join(filename))

def test_when_obsolete_day_is_today_then_dont_delete_it(mocker, tmpdir):
    mocker.patch('lxd_backup.backup.today', return_value='1995-12-25')
    export_dir = tmpdir.join('images')
    os.makedirs(export_dir, exist_ok=True)
    config = {'dir': export_dir}

    filename = '1992-10-26_until_1995-12-25_test-container'
    open(export_dir.join(filename), 'w+').close() 

    cleanup(config)

    assert os.path.isfile(export_dir.join(filename))
