# lxd-backup
Tools for automating backup of lxd containers

[![Build Status](https://travis-ci.org/apeyrard/lxd-backup.svg?branch=master)](https://travis-ci.org/apeyrard/lxd-backup)
[![Maintainability](https://api.codeclimate.com/v1/badges/8ad1a716dc5cd2f6dc9a/maintainability)](https://codeclimate.com/github/apeyrard/lxd-backup/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/8ad1a716dc5cd2f6dc9a/test_coverage)](https://codeclimate.com/github/apeyrard/lxd-backup/test_coverage)
[![codecov](https://codecov.io/gh/apeyrard/lxd-backup/branch/master/graph/badge.svg)](https://codecov.io/gh/apeyrard/lxd-backup)

[x] publish images for containers

[x] export images to storage

[x] export images to aws s3

[x] use config file to parameterize options per container

[x] create systemd oneshot service

[x] export only once when several backups

[x] allow choosing frequency

[x] allow specification of lifetime

[x] delete obsolete images from storage

[x] allow custom commands to be run in container before and after backup

[ ] export images to ftp

[ ] readthedocs

[ ] email on failure
