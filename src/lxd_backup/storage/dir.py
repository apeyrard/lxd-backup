import os
import shutil
import arrow

from ..time import today


class Dir():

    def __init__(self, path):
        self.__path = path
        os.makedirs(path, exist_ok=True)

    def export(self, image):
        out_file_path = os.path.join(self.__path, image.aliases[0]['name'])
        in_file = image.export()
        with open(out_file_path, 'wb') as out_file:
            shutil.copyfileobj(in_file, out_file)
        image.delete()

    def cleanup(self):
        for f in os.listdir(self.__path):
            if 'until' in f:
                limit = f.split('_')[2]
                if arrow.get(limit).format('YYYY-MM-DD') < today():
                    os.remove(os.path.join(self.__path, f))

    def exists(self, file):
        return os.path.isfile(os.path.join(self.__path, file))

    def delete_all(self):
        shutil.rmtree(self.__path)

    def create_file(self, path):
        open(os.path.join(self.__path, path), 'w+').close() 

