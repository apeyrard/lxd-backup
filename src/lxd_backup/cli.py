import sys
import argparse
import json

from lxd_backup.frequencies import should_backup, Frequency
from lxd_backup.backup import backup_container
from lxd_backup.storage.dir import Dir
from lxd_backup.storage.s3 import S3

def parse_args(args):
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config')
    return parser.parse_args()


def parse_config(config):
    with open(config, 'rb') as f:
        config = json.load(f)
    for container in config:
        container_config = config[container]
        before_script = container_config["before_script"] if "before_script" in container_config else None
        after_script = container_config["after_script"] if "after_script" in container_config else None
        for rule in container_config["rules"]:
            frequency = rule['frequency']
            when = rule['when'] if 'when' in rule else None
            if should_backup(Frequency[rule['frequency']], when):
                backup_config = {'lifetime': rule['lifetime']}
                if before_script is not None:
                    backup_config['before_script'] = before_script
                if after_script is not None:
                    backup_config['after_script'] = after_script
                image = backup_container(container, backup_config)
                if rule['storage'] == 'dir':
                    Dir(rule['path']).export(image)
                elif rule['storage'] == 's3':
                    S3(rule['path']).export(image)
    


def main():
    args = parse_args(sys.argv[1:])
    parse_config(args.config)

if __name__ == '__main__':
    main()
