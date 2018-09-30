import os
import shutil
import arrow

from ..time import today


class Dir():

    def __init__(self, path):
        self.__path = path
        os.makedirs(path, exist_ok=True)

    def export(self, image):
        out_file_path = self.__path.join(image.aliases[0]['name'])
        in_file = image.export()
        with open(out_file_path, 'wb') as out_file:
            shutil.copyfileobj(in_file, out_file)
        image.delete()

    def cleanup(self):
        for f in os.listdir(self.__path):
            if 'until' in f:
                limit = f.split('_')[2]
                if arrow.get(limit).format('YYYY-MM-DD') < today():
                    os.remove(self.__path.join(f))

    def exists(self, file):
        return os.path.isfile(self.__path.join(file))

    def delete_all(self):
        shutil.rmtree(self.__path)

    def create_file(self, path):
        open(self.__path.join(path), 'w+').close() 

