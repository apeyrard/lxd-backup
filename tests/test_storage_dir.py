import os
from arrow import utcnow

from lxd_backup.backup import backup_container
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
    
    


