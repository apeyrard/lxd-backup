# lxd-backup
Tools for automating backup of lxd containers

[x] publish images for containers

[x] export images to storage

[x] export images to aws s3

[x] use config file to parameterize options per container

[ ] create systemd oneshot service

[ ] export only once when several backups

[x] allow choosing frequency

[x] allow specification of lifetime

[x] delete obsolete images from storage

[x] allow custom commands to be run in container before and after backup

[ ] export images to aws glacier (warning, deletion before 90 days are billed for 90 days. include that in doc, maybe disallow glacier for lower than monthly lifetimes)

[ ] export images to nextcloud

[ ] export images to ftp

[ ] readthedocs

[ ] email on failure
