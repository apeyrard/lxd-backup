import sys
import argparse
import json
import logging

from lxd_backup.frequencies import should_backup, Frequency
from lxd_backup.backup import backup_container
from lxd_backup.storage.dir import Dir
from lxd_backup.storage.s3 import S3
from lxd_backup.time import get_date_from_lifetime

logger = logging.getLogger(__name__)

def parse_args(args):
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config')
    return parser.parse_args()


def parse_config(config):

    with open(config, 'rb') as f:
        config = json.load(f)

    for container in config:
        container_config = config[container]

        rule = longest_lived_rule(container_config)

        backup_config = {'lifetime': rule['lifetime'],
                         'before_script': container_config.get("before_script"),
                         'after_script': container_config.get("after_script")}

        image = backup_container(container, backup_config)
        storage = get_storage_backend(rule)
        storage.export(image)
        storage.cleanup()


def longest_lived_rule(config):
    longest_lifetime = "0000-00-00"
    for rule in config["rules"]:
        when = rule.get('when')
        last_valid_date = get_date_from_lifetime(rule['lifetime'])
        if should_backup(Frequency[rule['frequency']], when) and last_valid_date > longest_lifetime:
            longest_lifetime = last_valid_date
            longest_lived_rule = rule
    return longest_lived_rule


def main():
    args = parse_args(sys.argv[1:])
    parse_config(args.config)


def get_storage_backend(rule):
    if rule['storage'] == 'dir':
        storage = Dir(rule['path'])
    elif rule['storage'] == 's3':
        storage = S3(rule['path'])
    return storage


if __name__ == '__main__':
    try:
        main()
    except exception as e:
        logger.exception(e)
