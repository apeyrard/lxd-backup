import os
import shutil
import arrow
import logging

from ..time import today
from . import get_md5


logger = logging.getLogger(__name__)


class Dir():

    def __init__(self, path):
        self.__path = path
        os.makedirs(path, exist_ok=True)

    def export(self, image):
        logger.info(f"exporting image: {image.aliases[0]['name']}")
        out_file_path = os.path.join(self.__path, image.aliases[0]['name'])
        in_file = image.export()
        md5sum = get_md5(in_file)
        with open(out_file_path, 'wb') as out_file:
            shutil.copyfileobj(in_file, out_file)
        with open(''.join([out_file_path, '.md5']), 'w') as out_file_hash:
            out_file_hash.write(md5sum)
        image.delete()

    def cleanup(self):
        for f in os.listdir(self.__path):
            if 'until' in f:
                limit = f.split('_')[2]
                if arrow.get(limit).format('YYYY-MM-DD') < today():
                    logger.info(f"deleting obsolete image: {f}")
                    os.remove(os.path.join(self.__path, f))

    def exists(self, file):
        return os.path.isfile(os.path.join(self.__path, file))

    def delete_all(self):
        shutil.rmtree(self.__path)

    def create_file(self, path):
        open(os.path.join(self.__path, path), 'w+').close() 

