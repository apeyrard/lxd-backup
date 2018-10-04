import hashlib
import arrow

from ..time import today


def get_md5(in_file):
    BLOCKSIZE = 65536
    buf = in_file.read(BLOCKSIZE)
    md5sum = hashlib.md5()
    while len(buf) > 0:
        md5sum.update(buf)
        buf = in_file.read(BLOCKSIZE)
    in_file.seek(0)
    return md5sum.hexdigest()


def is_file_obsolete(filename):
    if 'until' in filename:
        limit = filename.split('_')[2]
        return arrow.get(limit).format('YYYY-MM-DD') < today()

