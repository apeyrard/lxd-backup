import os

from lxd_backup import publish_container
from fixtures import given_container, client


def test_unkown_container(client):
    publish_container("unknown")

    assert not client.images.exists("2018-09-22_a-unknown", alias=True)

def test_publish_one_container_then_image_exists(given_container, client):
    given_container("a-container")

    publish_container("a-container")
    result = client.images.exists("2018-09-22_a-container", alias=True)

    client.images.get_by_alias("2018-09-22_a-container").delete()

    assert result

def test_publish_one_container_then_container_is_running(given_container, client):
    given_container("another-container")

    publish_container("another-container")
    client.images.get_by_alias("2018-09-22_another-container").delete()
    assert client.containers.get("another-container").status == 'Running'
