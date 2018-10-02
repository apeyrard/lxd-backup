import hashlib

def get_md5(in_file):
    BLOCKSIZE = 65536
    buf = in_file.read(BLOCKSIZE)
    md5sum = hashlib.md5()
    while len(buf) > 0:
        md5sum.update(buf)
        buf = in_file.read(BLOCKSIZE)
    in_file.seek(0)
    return md5sum.hexdigest()
