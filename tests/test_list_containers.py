import pytest

from lxd_backup import list_containers

def test_no_containers():
    assert [] == list_containers()
