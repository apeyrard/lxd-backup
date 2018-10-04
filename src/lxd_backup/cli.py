import sys
import argparse
import json

from lxd_backup.frequencies import should_backup, Frequency
from lxd_backup.backup import backup_container
from lxd_backup.storage.dir import Dir
from lxd_backup.storage.s3 import S3
from lxd_backup.time import get_date_from_lifetime

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
        before_script = container_config.get("before_script")
        after_script = container_config.get("after_script")

        when = rule.get('when')
        if should_backup(Frequency[rule['frequency']], when):
            backup_config = {'lifetime': rule['lifetime']}
            if before_script is not None:
                backup_config['before_script'] = before_script
            if after_script is not None:
                backup_config['after_script'] = after_script
            image = backup_container(container, backup_config)
            if rule['storage'] == 'dir':
                storage = Dir(rule['path'])
            elif rule['storage'] == 's3':
                storage = S3(rule['path'])
            storage.export(image)
            storage.cleanup()


def longest_lived_rule(config):
    longest_lifetime = None
    longest_lived_rule = None
    for rule in config["rules"]:
        when = rule.get('when')
        if should_backup(Frequency[rule['frequency']], when):
            last_valid_date = get_date_from_lifetime(rule['lifetime'])
            if longest_lifetime is None or last_valid_date > longest_lifetime:
                longest_lifetime = last_valid_date
                longest_lived_rule = rule
    return longest_lived_rule
    

def main():
    try:
        args = parse_args(sys.argv[1:])
        parse_config(args.config)
    except exception as e:
        logger.exception(e)

if __name__ == '__main__':
    main()
