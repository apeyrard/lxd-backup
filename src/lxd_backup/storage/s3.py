import boto3
import botocore
import logging
import io

from ..time import today
from . import get_md5, is_file_obsolete


logger = logging.getLogger(__name__)


class S3():

    def __init__(self, bucket):
        self._bucket_name = bucket
        self._s3 = boto3.resource('s3')
        self._bucket = self._s3.Bucket(bucket)
        try:
            self._bucket.create()
        except:
            pass

    def export(self, image):
        logger.info(f"exporting image: {image.aliases[0]['name']}")
        in_file = image.export()
        md5sum = get_md5(in_file)
        self._bucket.upload_fileobj(in_file, image.aliases[0]['name'])
        self._bucket.upload_fileobj(io.BytesIO(md5sum.encode()), ''.join([image.aliases[0]['name'], '.md5']))
        image.delete()

    def exists(self, file):
        try:
            self._s3.Object(self._bucket_name, file).load()
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == "404":
                return False
            else:
                raise
        else:
            return True

    def delete_all(self):
        self._bucket.objects.all().delete()
        self._bucket.delete()

    def create_file(self, path):
        self._bucket.put_object(Key=path, Body='test')

    def cleanup(self):
        for file in self._bucket.objects.all():
            if is_file_obsolete(file.key):
                logger.info(f"deleting obsolete image: {file.key}")
                self.delete_file(file.key)

    def delete_file(self, filename):
        self._bucket.delete_objects(Delete={'Objects': [{'Key': filename}]})
